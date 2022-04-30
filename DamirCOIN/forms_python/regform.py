from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, Email


class RegForm(FlaskForm):
    username = StringField('Ваше имя', validators=[DataRequired()])
    email = EmailField('Эл.почта', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeatpassword = StringField('Повтор пароля')
    submit = SubmitField('Регистрация')
