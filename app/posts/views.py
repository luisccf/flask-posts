from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import app, db, models, login_manager
from forms import PostForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime


mod = Blueprint(
    'posts', __name__, static_folder='./static', template_folder='./templates')


@mod.route('/posts/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = models.Post(
                text=form.text.data, timestamp=datetime.datetime.utcnow(), user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.posts'))
    return render_template('add_post.html', title='Add Post', users=models.User.query.all(), form=form)


@mod.route('/posts')
def posts():
    return render_template('posts.html', title='All Posts', posts=models.Post.query.all(), user_page=0)


@mod.route('/posts/<int:post_id>')
def post(post_id):
    post = models.Post.query.get_or_404(post_id)
    return render_template('post.html', title='Post', post=post)


@mod.route('/posts/<int:post_id>/remove-<int:user_page>')
@login_required
def remove(post_id, user_page):
    post = models.Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        return 401
    user = post.author
    db.session.delete(post)
    db.session.commit()
    if user_page == 1:
        return redirect(url_for('users.user', nickname=user.nickname))
    return redirect(url_for('posts.posts'))


@mod.route('/posts/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = models.Comment(
                user_id=current_user.id, post_id=post_id, text=form.text.data)
            db.session.add(comment)
            db.session.commit()
            post = models.Post.query.get(post_id)
            return redirect(url_for('posts.post', post_id=post_id))
    return render_template('add_post.html', title='Add comment', post_id=post_id, form=form)
