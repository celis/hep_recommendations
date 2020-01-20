from flask import Flask, render_template
from gensim.models import KeyedVectors
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from inspirehep_api_wrapper.service.inspire_api import InspireAPI
import boto3
import configparser
import os


class Configuration:
    """
    Class for the configuration of the S3 access and the model artifact
    """

    CONFIG_FILE = "configs/config.ini"

    def __init__(self):
        self._parser = configparser.ConfigParser()
        self._parser.read(self.CONFIG_FILE)

    @property
    def s3(self):
        """
        config parameters for S3 access
        """
        if os.path.exists(self.CONFIG_FILE):
            config = self._parser["s3"]
            return {
                "region_name": config.get("region_name", ""),
                "bucket": config.get("bucket", ""),
                "access_key": config.get("access_key", ""),
                "secret_key": config.get("secret_key", ""),
            }
        else:
            return {
                "region_name": os.environ["AWS_S3_REGION"],
                "bucket": os.environ["S3_BUCKET_NAME"],
                "access_key": os.environ["AWS_ACCESS_KEY_ID"],
                "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            }

    @property
    def model_artifact(self):
        """
        config parameters for the model artifact
        """
        if os.path.exists(self.CONFIG_FILE):
            config = self._parser["model_artifact"]
            return config.get("path", "")
        else:
            return os.environ["MODEL_ARTIFACT_PATH"]

class InputForm(FlaskForm):
    """
    Allows users to enter an INSPIRE article id
    """

    article = StringField("Enter an INSPIRE article id", validators=[DataRequired()])
    submit = SubmitField("Submit")


class GensimWrapper:
    """
    Wrapper around Gensim library with the basic functionalities we need, loading trained embeddings
    and predicting the most similar items
    """

    def __init__(self):
        self._model = None

    def load(self, model_path: str):
        """
        Loads trained embeddings
        """
        self._model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    def most_similar(self, article: str, topn: int = 5):
        """
        Predicts most similar items
        """
        return [article[0] for article in self._model.similar_by_word(article, topn)]

    def vocabulary(self):
        """
        Returns all articles which have embeddings
        """
        return [recid for recid in self._model.vocab]


def download_model_artifacts(config: Configuration):
    """
    Downloads model artifact from S3
    """
    model_name, model_path = config.model_artifact.split("/")[-1], config.model_artifact

    if config.s3["access_key"] and config.s3["secret_key"]:
        access_key = config.s3["access_key"]
        secret_key = config.s3["secret_key"]


    boto3_client = boto3.client(
        "s3",
        region_name=config.s3["region_name"],
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    boto3_client.download_file(config.s3["bucket"], model_name, model_path)


def load_model(config: Configuration):
    """
    Loads trained model from disk if available, otherwise its first downloaded from S3.
    """

    if not os.path.exists(config.model_artifact):
        download_model_artifacts(config)

    model = GensimWrapper()
    model.load(config.model_artifact)
    return model


app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
bootstrap = Bootstrap()
bootstrap.init_app(app)

config = Configuration()

model = load_model(config)


@app.route("/", methods=["GET", "POST"])
def index():
    article = None
    recommendations = None
    form = InputForm()
    inspire_api = InspireAPI()
    if form.validate_on_submit():
        article = form.article.data
        if article in model.vocabulary():
            article = {
                "id": article,
                "record": inspire_api.literature(article).to_record(),
            }
            recommendations = model.most_similar(article["id"])
            recommendations = [
                {
                    "id": recommendation,
                    "record": inspire_api.literature(recommendation).to_record(),
                }
                for recommendation in recommendations
            ]
    return render_template(
        "index.html", form=form, article=article, recommendations=recommendations
    )


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
