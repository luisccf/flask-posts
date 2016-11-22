from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import app, db, models, login_manager
from forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime


mod = Blueprint('users', __name__, static_folder='./static', template_folder='./templates', url_prefix='/users')


@mod.route('/')
def users():
	return render_template('users.html', title='Users', users=models.User.query.all())


@mod.route('/<nickname>')
def user(nickname):
	return render_template('posts.html', title='User: ' + nickname, posts=db.session.query(models.User).filter_by(nickname=nickname).first().posts, user_page=1)


@mod.route('/signup', methods=['GET'])
def signup_get():
	form = SignupForm()
	return render_template('login.html', title='Sign up', form=form)


@mod.route('/signup', methods=['POST'])
def signup_post():
	form = SignupForm()
	if form.validate_on_submit():
		user = models.User(nickname=form.nickname.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('home.index'))
	return render_template('login.html', title='Sign up', form=form), 400


@mod.route('/login', methods=['GET'])
def login_get():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)


@mod.route('/login', methods=['POST'])
def login_post():
	form = LoginForm()
	if form.validate_on_submit():
		user = models.User.query.filter_by(nickname=form.nickname.data).first()
		login_user(user)
		return render_template('index.html', title='Home', user=user)
	return render_template('login.html', title='Login', form=form), 400


@mod.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home.index'))


@login_manager.user_loader
def load_user(user_id):
	return models.User.query.get(int(user_id))
