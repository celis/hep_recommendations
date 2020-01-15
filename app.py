from flask import Flask, request, render_template
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


@app.route('/', methods=['GET', 'POST'])
def index():
    id = None
    form = InputForm()
    if form.validate_on_submit():
        id = form.id.data
    return render_template('index.html', form=form, id=id)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
