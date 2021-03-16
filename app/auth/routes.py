from flask import Blueprint
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
import bcrypt
from app.models import User
from app.auth.forms import SignUpForm, LoginForm
# Import Forms

from app import app, db
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Route for user signup """
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)
