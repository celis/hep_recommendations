from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class InputForm(FlaskForm):
    """
    Allows users to enter an INSPIRE article id
    """

    class Meta:
        csrf = False

    article = StringField(
        "<h5> Enter an INSPIRE article id </h5>", validators=[DataRequired()]
    )
    submit = SubmitField("Find related articles")
