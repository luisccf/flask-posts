from flask import render_template, url_for, flash, redirect, request
from app import app, db, models
import datetime

@app.route('/')
def index():
	user = models.User.query.get(1)
	return render_template('index.html', title='Home', header='App', user=user)

@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		post = request.form.to_dict()
		new_post = models.Post(title=post['title'], timestamp=datetime.datetime.utcnow(), user_id=post['author'])
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
	
@app.route('/posts/remove/<int:user_page>/<int:post_id>')
def remove(post_id, user_page):
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
	if request.method == 'POST':
		comment = request.form.to_dict()
		author = models.User.query.get(comment['author'])
		new_comment = models.Comment(user_id=author.id, post_id=post_id, content=comment['content'])
		db.session.add(new_comment)
		db.session.commit()
		post = models.Post.query.get(post_id)
		return redirect(url_for('post', post_id=post_id))
	return render_template('comment.html', title='Add comment', header='Add comment', users=models.User.query.all(), post_id=post_id)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
	if request.method == 'POST':
		user = request.form.to_dict()
		db.session.add(models.User(nickname=user['nickname']))
		db.session.commit()
		return redirect(url_for('users'))
	return render_template('add_user.html', title='Sign up', header='Sign up')


