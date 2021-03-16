from flask import Blueprint, request, render_template, redirect, url_for, flash
import flask
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime

import flask_login
from app import bcrypt

from app.models import User, Party, Playlist
from app.main.forms import CreatePartyForm, JoinPartyForm 

from random import randint
from app import app, db

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('main/home.html')


# Create Party
@main.route('/create_party', methods=['GET', 'POST'])
def create_party():
    ''' This route permits the creation of a party. It also sets the creator as the admin'''
    form = CreatePartyForm()
    if form.validate_on_submit():
        new_party = Party(
            admin = flask_login.current_user,
            name = form.name.data,
            code = randint(1000000,9999999)
        )
        current_user.current_party.append(new_party)
        db.sesion.add(new_party)
        db.session.commit()
        flash('Party Created Successfully')
        return redirect(url_for('main.home', party=new_party))
    return render_template('main/create_party.html', form=form)
