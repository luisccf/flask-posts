import unittest
import os
import sqlalchemy
from app import app, db
import factory
from app.models import Post
from faker import Faker


class TestPost(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_posts_tests'


    def add_post(self, text):
        return self.tester.post('/posts/add', data=dict(
            text=text
        ), follow_redirects=True)


    def login(self, nickname, password):
        return self.tester.post('/login', data=dict(
            nickname=nickname,
            password=password
        ), follow_redirects=True)


    def test_add_post(self):
        faker = Faker()

        # no user logged in
        text = faker.text(max_nb_chars=140)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 401)

        response = self.login('admin', 'password')
        self.assertEqual(response.status_code, 200)
        
        # text shorter than 140 characters
        text = faker.text(max_nb_chars=200)
        while 0 <= text <= 140:
            text = faker.text(max_nb_chars=200)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 400)

        # text not empty
        response = self.add_post('')
        self.assertEqual(response.status_code, 400)

        # success
        text = faker.text(max_nb_chars=140)
        response = self.add_post(text)
        self.assertEqual(response.status_code, 200)
