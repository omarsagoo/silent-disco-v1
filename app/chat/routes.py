from flask import Blueprint, render_template
from .. import socketio

chat = Blueprint('chat', __name__)

@chat.route("/chat")
def sessions():
    return render_template('chat/session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)
