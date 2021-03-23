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
