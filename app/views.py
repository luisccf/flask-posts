from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, models, login_manager
from forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime

@app.route('/')
def index():
	return render_template('index.html', title='Home', header='App')

@app.route('/posts/add', methods=['GET', 'POST'])
def add():
	if current_user.is_authenticated == False:
		return render_template('error.html', error='Please login to post.')
	if request.method == 'POST':
		post = request.form.to_dict()
		new_post = models.Post(title=post['title'], timestamp=datetime.datetime.utcnow(), user_id=current_user.id)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for('posts'))
	return render_template('add.html', title='Add Post', header='New post', users=models.User.query.all())

@app.route('/posts')
def posts():
	return render_template('posts.html', title='Posts', header='All Posts', posts=models.Post.query.all())

@app.route('/posts/<int:post_id>')
def post(post_id):
	post = models.Post.query.get(post_id)
	#import pdb; pdb.set_trace()
	return render_template('post.html', title=post.title, header=post.title, post=post)
	
@app.route('/posts/<int:post_id>/remove-<int:user_page>')
def remove(post_id, user_page):
	if current_user.is_authenticated is False or current_user.id != models.Post.query.get(post_id).author.id:
		return render_template('error.html', error='You can\'t remove somebody else\'s post.')
	post = models.Post.query.get(post_id)
	user = post.author
	db.session.delete(post)
	db.session.commit()
	if user_page == 1:
		return redirect(url_for('user', nickname=user.nickname))
	return redirect(url_for('posts'))

@app.route('/users')
def users():
	return render_template('users.html', title='Users', header='Users', users=models.User.query.all())

@app.route('/users/<nickname>')
def user(nickname):
	return render_template('user.html', title='User: ' + nickname, header='User: ' + nickname, user=db.session.query(models.User).filter_by(nickname=nickname).first())

@app.route('/posts/<int:post_id>/comment', methods=['GET', 'POST'])
def comment(post_id):
	if current_user.is_authenticated is False:
		return render_template('error.html', error='Please login to comment.')
	if request.method == 'POST':
		comment = request.form.to_dict()
		new_comment = models.Comment(user_id=current_user.id, post_id=post_id, content=comment['content'])
		db.session.add(new_comment)
		db.session.commit()
		post = models.Post.query.get(post_id)
		return redirect(url_for('post', post_id=post_id))
	return render_template('comment.html', title='Add comment', header='Add comment', users=models.User.query.all(), post_id=post_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated is True:
		return render_template('error.html', error='You\'re already logged in')
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			response = request.form.to_dict()
			if db.session.query(models.User).filter_by(nickname=response['nickname']).first():
				return render_template('login.html', header='Sign up', form=form, message='Nickname already taken!')
			user = models.User(nickname=response['nickname'], password=response['password'])
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('index'))
		return render_template('login.html', header='Sign up', form=form, message='Please enter nickname and password!')
	return render_template('login.html', title='Sign up', header='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated is True:
		return render_template('error.html', error='You\'re already logged in')
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = user_logging_in(form)
			if user is None:
				return render_template('login.html', header='Sign in', form=form, message='Wrong username or password!')
			login_user(user)
			return render_template('index.html', title='Home', header='App', user=user)
		return render_template('login.html', header='Sign in', form=form, message='Please enter nickname and password!')
	return render_template('login.html', header='Sign in', form=form)

def user_logging_in(form):
	user = db.session.query(models.User).filter_by(nickname=form.nickname.data).first()
	if user is None or form.password.data != user.password:
		return None
	return user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
	return models.User.query.get(int(user_id))




