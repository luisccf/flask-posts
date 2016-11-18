from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import app, db, models, login_manager
from forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime

mod = Blueprint('users', __name__, static_folder='./static', template_folder='./templates')

@mod.route('/users')
def users():
	return render_template('users.html', title='Users', users=models.User.query.all())

@mod.route('/users/<nickname>')
def user(nickname):
	return render_template('posts.html', title='User: ' + nickname, posts=db.session.query(models.User).filter_by(nickname=nickname).first().posts, user_page=1)

@mod.route('/signup', methods=['GET', 'POST'])
def signup():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			response = request.form.to_dict()
			if db.session.query(models.User).filter_by(nickname=response['nickname']).first():
				flash('Nickname already taken!', 'danger')
				return render_template('login.html', title='Sign up', form=form), 401
			user = models.User(nickname=response['nickname'], password=response['password'])
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('home.index'))
		flash('Please enter a nickname and a password!', 'danger')
		return render_template('login.html', title='Sign up', form=form), 402
	return render_template('login.html', title='Sign up', header='Sign up', form=form)

@mod.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		form = LoginForm(request.form)
		if form.validate_on_submit():
			user = user_logging_in(form)
			if user is None:
				flash('Wrong username or password!', 'danger')
				return render_template('login.html', title='Login', form=form), 401
			login_user(user)
			return render_template('index.html', title='Home', header='App', user=user), 200
		flash('Please enter a nickname and a password!', 'danger')
		return render_template('login.html', title='Login', form=form), 402
	return render_template('login.html', title='Login', form=LoginForm())

def user_logging_in(form):
	user = db.session.query(models.User).filter_by(nickname=form.nickname.data).first()
	if user is None or form.password.data != user.password:
		return None
	return user

@mod.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home.index'))

@login_manager.user_loader
def load_user(user_id):
	return models.User.query.get(int(user_id))




