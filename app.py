from flask import Flask, render_template
from gensim.models import KeyedVectors
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from inspirehep_api_wrapper.service.inspire_api import InspireAPI
import boto3


def download_model_artifacts():
    s3_resource = boto3.resource("s3")
    s3_resource.Bucket("similar-articles-data").download_file(
        "article_embeddings.bin", "model_artifact/article_embeddings.bin"
    )


app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
bootstrap = Bootstrap()
bootstrap.init_app(app)


class InputForm(FlaskForm):
    article = StringField("article", validators=[DataRequired()])

    submit = SubmitField("Submit")


class GensimWrapper:
    """
    """

    def __init__(self):
        """
        :param
        """
        self._model = None

    def load(self, model_path):
        self._model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    def most_similar(self, article: str, topn: int = 5):
        """
        """
        return [article[0] for article in self._model.similar_by_word(article, topn)]

    def vocabulary(self):
        """
        Returns all record ids which have embeddings
        """
        return [recid for recid in self._model.vocab]


download_model_artifacts()

model = GensimWrapper()
model.load("model_artifact/article_embeddings.bin")


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
