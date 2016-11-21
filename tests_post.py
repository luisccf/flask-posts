import unittest
import os
import sqlalchemy
from app import app, db
import factory
from app.models import Post, User
from faker import Faker


class TestPost(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['WTF_CSRF_ENABLED'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_posts_tests'

    def add_post(self, text):
        return self.tester.post('/posts/add', data=dict(
            text=text
        ), follow_redirects=True)

    def remove_post(self, post_id):
        return self.tester.get('/posts/' + str(post_id) + '/remove-0', follow_redirects=True)

    def login(self, nickname, password):
        return self.tester.post('/login', data=dict(
            nickname=nickname,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.tester.get('/logout', follow_redirects=True)

    def test_add_post(self):
        faker = Faker()

        # Fails because no user is logged in
        text = faker.text(max_nb_chars=140)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 401)

        response = self.login('admin', 'password')
        self.assertEqual(response.status_code, 200)

        # Fails because text is longer than 140 characters
        text = faker.text(max_nb_chars=200)
        while 0 <= text <= 140:
            text = faker.text(max_nb_chars=200)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 400)

        # Fails because text is empty
        response = self.add_post('')
        self.assertEqual(response.status_code, 400)

        # Success
        text = faker.text(max_nb_chars=140)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 200)

    def test_remove_post(self):
        faker = Faker()

        # Logs in, posts something and logs out
        response = self.login('admin', 'password')
        self.assertEqual(response.status_code, 200)

        text = faker.text(max_nb_chars=140)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 200)

        response = self.logout()
        self.assertEqual(response.status_code, 200)

        # Gets last added post
        user = User.query.filter_by(nickname='admin').first()
        post = Post.query.filter_by(user_id=user.id).order_by(
            Post.timestamp.desc()).first()

        # Tries to delete it, but fails because no user is logged in
        response = self.remove_post(post.id)
        self.assertEqual(response.status_code, 401)

        # Logs author in and deletes post
        response = self.login('admin', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.remove_post(post.id)
        self.assertEqual(response.status_code, 200)
