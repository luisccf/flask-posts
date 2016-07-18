from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import app, db, models, login_manager
from flask_login import login_user, logout_user, current_user, login_required
import datetime

mod = Blueprint('posts', __name__, static_folder='./content', template_folder='./templates')

@mod.route('/posts/add', methods=['GET', 'POST'])
def add():
	if current_user.is_authenticated == False:
		return render_template('error.html', error='Please login to post.')
	if request.method == 'POST':
		post = request.form.to_dict()
		new_post = models.Post(title=post['title'], timestamp=datetime.datetime.utcnow(), user_id=current_user.id)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for('posts.posts'))
	return render_template('add_post.html', title='Add Post', header='New post', users=models.User.query.all())

@mod.route('/posts')
def posts():
	return render_template('posts.html', title='Posts', header='All Posts', posts=models.Post.query.all())

@mod.route('/posts/<int:post_id>')
def post(post_id):
	post = models.Post.query.get(post_id)
	if post is None:
		return render_template('error.html', error='No post with id ' + str(post_id))
	#import pdb; pdb.set_trace()
	return render_template('post.html', title=post.title, header=post.title, post=post)
	
@mod.route('/posts/<int:post_id>/remove-<int:user_page>')
def remove(post_id, user_page):
	if current_user.is_authenticated is False or current_user.id != models.Post.query.get(post_id).author.id:
		return render_template('error.html', error='You can\'t remove somebody else\'s post.')
	post = models.Post.query.get(post_id)
	user = post.author
	db.session.delete(post)
	db.session.commit()
	if user_page == 1:
		return redirect(url_for('users.user', nickname=user.nickname))
	return redirect(url_for('posts.posts'))

@mod.route('/posts/<int:post_id>/comment', methods=['GET', 'POST'])
def comment(post_id):
	if current_user.is_authenticated is False:
		return render_template('error.html', error='Please login to comment.')
	if request.method == 'POST':
		comment = request.form.to_dict()
		new_comment = models.Comment(user_id=current_user.id, post_id=post_id, content=comment['content'])
		db.session.add(new_comment)
		db.session.commit()
		post = models.Post.query.get(post_id)
		return redirect(url_for('posts.post', post_id=post_id))
	return render_template('comment.html', title='Add comment', header='Add comment', users=models.User.query.all(), post_id=post_id)




