from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import app, db, models, login_manager
from flask_login import login_user, logout_user, current_user, login_required
import datetime
import pymysql

mod = Blueprint('home', __name__, static_folder='./content', template_folder='./templates')

@mod.route('/')
def index():
	return render_template('index.html', title='Home', header='App')