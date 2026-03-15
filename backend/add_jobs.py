from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField("Название работы", validators=[DataRequired()])
    team_leader = StringField("Лидер", validators=[DataRequired()])
    work_size = IntegerField("Продолжительность", validators=[DataRequired()])
    colloborators = StringField("Работники", validators=[DataRequired()])
    finished = BooleanField("Статус конца работы")
    submit = SubmitField("Применить")