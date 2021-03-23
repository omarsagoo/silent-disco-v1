import os
from unittest import TestCase

from datetime import date
from app import app, db, bcrypt
from app.models import User


# Helper Functions

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash, name='test')
    db.session.add(user)
    db.session.commit()


# Tests


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup_existing_user(self):
        # Tests for the signup route. It should:
        # - Create a user
        # - Make a POST request to /signup, sending the same username & password
        # - Check that the form is displayed again with an error message
        post_data = {
            'username': 'Test User',
            'password': '12345',
            'name': 'John'
        }
        self.app.post('/signup', data=post_data)

        post_data = {
            'username': 'Test User',
            'password': '12345',
            'name': 'John'
        }
        response = self.app.post('/signup', data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn(
            'That username is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):
        # Tests for the login route. It should:
        # - Create a user
        # - Makes a POST request to /login, sending the created username & password
        # - Check that the homepage  now displays the logout button (indicating that user is
        # authenticated)

        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/login', data=post_data)

        response = self.app.get('/', follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertIn('logout', response_text)

    def test_login_incorrect_password(self):
        # Tests for the login route. It should:
        # - Create a user
        # - Make a POST request to /login, sending the created username &
        #   an incorrect password
        # - Checks that the login form is displayed again, with an appropriate
        #   error message

        create_user()

        post_data = {
            'username': 'me1',
            'password': '1234567'
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn(
            "Password doesn&#39;t match. Please try again.", response_text)
