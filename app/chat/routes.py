from flask import Blueprint, render_template
from flask.signals import Namespace
from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room

from .. import socketio, db
from ..models import Party, Message
from .forms import SendMessageForm 


chat = Blueprint('chat', __name__)

@chat.route("/chat/<party_id>")
@login_required
def sessions(party_id):
    form = SendMessageForm()
    party = Party.query.get(party_id)
    return render_template('chat/session.html', form=form, messages=party.messages)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('message')
def handle_message_received(data, methods=['GET', 'POST']):
    print(f'received my event from {current_user.name}: '+ str(data))
    data['name'] = current_user.name


    if data['message'] == 'dIsCOnNECTED USeR':
        leave_room(data['party_id'])
        print("left")
        return

    new_msg = Message(
        name = current_user.name,
        message = data['message']
    )
    party = Party.query.get(data['party_id'])
    party.messages.append(new_msg)
    db.session.commit()

    socketio.emit('recieved message', data, callback=messageReceived, to=data['party_id'])


@socketio.on("disconnection")
def disconnect_client(data, methods=['GET', 'POST']):
    leave_room(data['party_id'])
    print("left")

@socketio.on('connection')
def connect_client(data, methods=['GET', 'POST']):
    join_room(data['party_id'])
    print("here")