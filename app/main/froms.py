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


# Join Party Form

class JoinPartyForm(FlaskForm):
    '''Form for joining a party. It checks the special code 
    to ensure the user is joining an existing party'''
    code = StringField("Code", validators=[
                       DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit!')

    def validate_code(self, code):
        party = Party.query.filter_by(code=code.data).first()
        if not party:
            raise ValidationError(
                'That code is incorrect. Please try again.')
