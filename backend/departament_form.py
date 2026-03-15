from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartamentsForm(FlaskForm):
    title = StringField("Название департамента", validators=[DataRequired()])
    chief = StringField("Шеф", validators=[DataRequired()])
    members = StringField("Работники", validators=[DataRequired()])
    email = StringField("Почта департамента", validators=[DataRequired()])
    submit = SubmitField("Применить")