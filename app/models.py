from sqlalchemy_utils import URLType

from app import db
from flask_login import UserMixin

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from random import randint

user_party_table = db.Table('user_party_table',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('party_id', db.Integer, db.ForeignKey('party.id'))
)

playlist_party_table = db.Table('playlist_party_table',
                                  db.Column('party_id', db.Integer, db.ForeignKey('party.id')),
                                  db.Column('playlist_id', db.Integer,db.ForeignKey('playlist.id'))
                                  )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    current_party = db.relationship('Party', secondary=user_party_table)
    past_parties = db.relationship('Party', secondary=user_party_table)

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin = db.relationship('User')
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.Integer, unique=True)
    party_people = db.relationship('User', secondary=user_party_table)
    playlist = db.relationship('Playlist', secondary=playlist_party_table)
    #TODO:
    # chat = 

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_song = db.Column(db.String(), nullable=False)
    party = db.relationship('Party', secondary=playlist_party_table)
    #TODO:
    # songs = array of Song

#TODO:
# Chat Model
