import unittest
import os
import sqlalchemy
import sys
from app import app, db
import factory
from app.models import User, Post, Comment
from config import SQLALCHEMY_DATABASE_URI
from faker import Faker


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
    
    nickname = factory.LazyAttribute(lambda x: fake.name())
    password = '123456'


class TestUser(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

        user = User(nickname='admin', password='password')
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()


    def login(self, nickname, password):
        return self.tester.post('/login', data=dict(
            nickname=nickname,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.tester.get('/logout', follow_redirects=True)


    def signup(self, nickname, password):
        fake = Faker()
        return self.tester.post('/signup', data=dict(
            nickname=nickname,
            password=password
        ), follow_redirects=True)


    def test_login_logout(self):
        # Login and logout with success
        response = self.login('admin', 'password')
        self.assertEqual(response.status_code, 200)

        response = self.logout()
        self.assertEqual(response.status_code, 200)

        # Wrong username or password
        response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 400)

        response = self.login('123456', '123456')
        self.assertEqual(response.status_code, 400)

        # Form has blank fields
        response = self.login('', 'password')
        self.assertEqual(response.status_code, 400)

        response = self.login('admin', '')
        self.assertEqual(response.status_code, 400)

        response = self.login('', '')
        self.assertEqual(response.status_code, 400)


    def test_signup_and_login(self):
        # Sign up with success
        nickname = Faker().name()
        response = self.signup(nickname, '123456')
        self.assertEqual(response.status_code, 200)

        response = self.logout()
        self.assertEqual(response.status_code, 200)

        # Fail login
        response = self.login(nickname, '123')
        self.assertEqual(response.status_code, 400)

        # Login with success
        response = self.login(nickname, '123456')
        self.assertEqual(response.status_code, 200)

        response = self.logout()
        self.assertEqual(response.status_code, 200)

        # Fail signup because user already exists
        response = self.signup('admin', '123456')
        self.assertEqual(response.status_code, 400)

        # Fail signup because form has blank fields
        response = self.signup('', '')
        self.assertEqual(response.status_code, 400)

        response = self.signup('', '123456')
        self.assertEqual(response.status_code, 400)
