from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import bcrypt
from app.models import User

# : Create Sign Up Form


class SignUpForm(FlaskForm):
    '''This form creates a new user'''
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')
