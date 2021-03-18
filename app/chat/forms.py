from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class SendMessageForm(FlaskForm):
    '''Form for sending a message'''
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Send')