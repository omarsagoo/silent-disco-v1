from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .forms import SendMessageForm 

from .. import socketio

chat = Blueprint('chat', __name__)

@chat.route("/chat")
@login_required
def sessions():
    form = SendMessageForm()
    return render_template('chat/session.html', form=form)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print(f'received my event from {current_user.name}: '+ str(json))
    json['name'] = current_user.name
    socketio.emit('my response', json, callback=messageReceived)
