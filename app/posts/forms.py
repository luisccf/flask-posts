from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class PostForm(Form):
    text = StringField('text', validators=[DataRequired('You haven\'t typed anything.'), Length(
        max=140, message='Posts must have 140 characters at max.')], widget=TextArea())
