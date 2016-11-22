from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User


class UserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired('Please enter a nickname.'), Length(max=64)])
    password = PasswordField('password', validators=[DataRequired('Please enter a password.'), Length(max=64)])


class SignupForm(UserForm):
	def validate_nickname(form, field):
		if User.query.filter_by(nickname=field.data).first():
			raise ValidationError('Nickname already taken.')


class LoginForm(UserForm):
	def validate_nickname(form, field):
		user = User.query.filter_by(nickname=form.nickname.data).first()
		if user is None:
			raise ValidationError('User not found.')
		if user.password != form.password.data:
			raise ValidationError('Wrong nickname or password.')
