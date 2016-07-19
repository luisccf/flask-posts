from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class PostForm(Form):
    text = StringField('text', validators=[DataRequired()], widget=TextArea())