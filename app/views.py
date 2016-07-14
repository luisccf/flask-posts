from flask import render_template, url_for, flash, redirect, request
from app import app, db, models
import datetime

@app.route('/')
def index():
	return render_template('index.html', title='Home', header='Posts', posts=models.Post.query.all(), authors=models.User.query.all())

@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		post = request.form.to_dict()
		new_post = models.Post(title=post['title'], timestamp=datetime.datetime.utcnow(), user_id=post['author'])
		db.session.add(new_post)
		db.session.commit()
		return render_template('index.html', title='Home', posts=models.Post.query.all())
	return render_template('add.html', title='Add Post', header='New post', users=models.User.query.all())

@app.route('/posts', methods=['GET', 'DELETE', 'POST'])
def posts():
	if request.method == 'DELETE':
		return render_template('success.html', title='Success')
	return render_template('posts.html', title='Posts', header='All Posts', posts=models.Post.query.all())
	
@app.route('/posts/remove/<int:post_id>')
def remove(post_id):
	db.session.delete(models.Post.query.get(post_id))
	db.session.commit()
	return render_template('success.html', title='Success')

@app.route('/users')
def users():
	return render_template('users.html', title='Users', header='Users', users=models.User.query.all())
