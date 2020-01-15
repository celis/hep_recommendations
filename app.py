from flask import Flask, render_template
from gensim.models import KeyedVectors
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap()
bootstrap.init_app(app)

class InputForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])

    submit = SubmitField('Submit')


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

model = GensimWrapper()
model.load("model/article_embeddings.bin")


@app.route('/', methods=['GET', 'POST'])
def index():
    id = None
    recommendations = None
    form = InputForm()
    if form.validate_on_submit():
        id = form.id.data
        if id in model.vocabulary():
            recommendations = model.most_similar(id)
    return render_template('index.html', form=form, id=id, recommendations=recommendations)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
