from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import models
from users.views import mod 
from posts.views import mod
from home.views import mod

app.register_blueprint(users.views.mod)
app.register_blueprint(posts.views.mod)
app.register_blueprint(home.views.mod)

