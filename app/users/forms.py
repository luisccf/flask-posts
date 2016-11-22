from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    nickname = StringField('nickname', validators=[DataRequired('Please enter a nickname.'), Length(max=64)])
    password = PasswordField('password', validators=[DataRequired('Please enter a password.'), Length(max=64)])
