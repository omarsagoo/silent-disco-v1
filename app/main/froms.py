from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from wtforms.fields.core import FloatField
from app import bcrypt
from app.models import User, Party, Playlist

# Create Party Form

class CreatePartyForm(FlaskForm):
    '''Form for creating a party'''
    name = StringField("Party Name", validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Create Party!')