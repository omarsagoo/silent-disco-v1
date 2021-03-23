from sqlalchemy.sql.sqltypes import ARRAY
from . import db
from flask_login import UserMixin

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from random import randint

user_party_table = db.Table('user_party_table',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('party_id', db.Integer, db.ForeignKey('party.id'))
                            )

# playlist_party_table = db.Table('playlist_party_table',
#                             db.Column('party_id', db.Integer, db.ForeignKey('party.id')),
#                             db.Column('playlist_id', db.Integer,db.ForeignKey('playlist.id'))
#                                   )

message_party_table = db.Table('message_party_table',
                            db.Column('party_id', db.Integer, db.ForeignKey('party.id')),
                            db.Column('message_id', db.Integer,db.ForeignKey('message.id'))
                                  )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    current_party = db.relationship("Party", back_populates="party_people")
    past_parties = db.relationship('Party', secondary=user_party_table)

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin = db.relationship('User')
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.Integer, unique=True)
    party_people = db.relationship('User', secondary=user_party_table)
    #playlist = db.relationship('Playlist', db.ForeignKey('playlist.id'))
    playlist = db.Column(db.String(80))
    #TODO:
    messages = db.relationship('Message', secondary=message_party_table)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(100), nullable=False)

