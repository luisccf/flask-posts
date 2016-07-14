from flask import Flask
from sqlalchemy import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

