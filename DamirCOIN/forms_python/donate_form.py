from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class DonateForm(FlaskForm):
    summ = StringField('Cумма', validators=[DataRequired()])
    submit = SubmitField('Отправить')