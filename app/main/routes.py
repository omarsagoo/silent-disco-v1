import json
from flask import Blueprint, request, render_template, redirect, url_for, flash
import flask
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime

import flask_login

from app.models import User, Party
from app.main.forms import CreatePartyForm, JoinPartyForm, PlaylistForm 

from random import randint
from app import app, db, bcrypt

import requests
import spotipy
import urllib.parse
import urllib.request
import re
from spotipy.oauth2 import SpotifyClientCredentials

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
        db.session.add(new_party)
        db.session.commit()
        flash('Party Created Successfully')
        return redirect(url_for('main.party_details', party_id=new_party.id))
    return render_template('main/create_party.html', form=form)


# Party Details
@main.route('/party/<party_id>')
@login_required
def party_details(party_id):
    party = Party.query.get(party_id)
    form = PlaylistForm()
    if party.playlist is not None:
        uid = party.playlist
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        #Need to pass access token into header to send properly formed GET request to API server
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        BASE_URL = 'https://api.spotify.com/v1/'

        r = requests.get(
            BASE_URL + 'search?q=SickoMode&type=track&market=US', headers=headers)
        d = r.json()
        print(r.text)

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id='b714b08a81b3470ab939354358c324c8', client_secret='83a32642aa4646009294ac6430b65dbe'))

        parsed = json.loads(r.text)
        (json.dumps(parsed, indent=4, sort_keys=True))

        songs = spotify.playlist_items(uid)
        tracks = []

        for i, playlist in enumerate(songs['items']):
            # [[Songs0, Artist0], [Songs1, Artist1]]
            tracks.append([songs['items'][i]['track']['name'],
                        songs['items'][i]['track']['artists'][0]['name']])

        for song in tracks:
            songToSearch = ' '.join([song[0], song[1]])
            query = urllib.parse.quote(songToSearch)

        print("Party details tracks", tracks)
        return render_template('main/party_detail.html', party=party, form=form, tracks=tracks)

    return render_template('main/party_detail.html', party=party, form=form)

    


# Join Party
@main.route('/join_party', methods=['GET', 'POST'])
@login_required
def join_party():
    form = JoinPartyForm()
    if form.validate_on_submit():
        party = Party.query.filter_by(code=form.code.data).one()
        current_user.past_parties.append(party)
        current_user.current_party = party
        db.session.commit()
        flash('Party was joined successfully')
        return redirect(url_for('main.party_details', party_id=party.id))
    return render_template('main/join_party.html', form=form)


CLIENT_ID = '69c20fe2830f4f2eab286331ffe88702'
CLIENT_SECRET = 'ed3cec28b71a4b6e8cd7997c17ed87d3'

AUTH_URL = 'https://accounts.spotify.com/api/token'


# Add Playlist Route
@main.route('/add_playlist/<party_id>', methods=['GET', 'POST'])
@login_required
def add_playlist(party_id):
    print("This works?")
    form = PlaylistForm()
    if form.validate_on_submit():
        uid = form.uid.data
        print(uid)

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

        # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    #Need to pass access token into header to send properly formed GET request to API server
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    BASE_URL = 'https://api.spotify.com/v1/'


    r = requests.get(
        BASE_URL + 'search?q=SickoMode&type=track&market=US', headers=headers)
    d = r.json()
    print(r.text)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id='b714b08a81b3470ab939354358c324c8', client_secret='83a32642aa4646009294ac6430b65dbe'))


    parsed = json.loads(r.text)
    (json.dumps(parsed, indent=4, sort_keys=True))

    songs = spotify.playlist_items(uid)
    tracks = []

    for i, playlist in enumerate(songs['items']):
        # [[Songs0, Artist0], [Songs1, Artist1]]
        tracks.append([songs['items'][i]['track']['name'],
                    songs['items'][i]['track']['artists'][0]['name']])

    for song in tracks:
        songToSearch = ' '.join([song[0], song[1]])
        query = urllib.parse.quote(songToSearch)
    print(tracks)
    party = Party.query.get(party_id)
    party.playlist = uid
    db.session.commit()

    return redirect(url_for('main.party_details', party=party, party_id=party.id, tracks=tracks))


    
