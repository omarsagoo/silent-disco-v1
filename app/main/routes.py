from flask import Blueprint, request, render_template, redirect, url_for, flash
import flask
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime

import flask_login

from app.models import User, Party, Playlist
from app.main.forms import CreatePartyForm, JoinPartyForm 

from random import randint
from app import app, db, bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('main/home.html')


# Create Party
@main.route('/create_party', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.homepage', party=new_party))
    return render_template('main/create_party.html', form=form)


# Party Details
@main.route('/party/<party_id>')
@login_required
def party_details(party_id):
    party = Party.query.get(party_id)
    return render_template('main/party_detail.html')


# Join Party
@main.route('/join_party', methods=['GET', 'POST'])
@login_required
def join_part():
    form = JoinPartyForm()
    if form.validate_on_submit():
        party = Party.query.filter_by(code=form.code.data).one()
        current_user.past_parties.append(party)
        current_user.current_party = party
        db.session.commit()
        flash('Party was created successfully')
        return redirect(url_for('main.homepage', party=party))
    return render_template('main/join_party.html', form=form)
