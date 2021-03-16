import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

socketio = SocketIO(app)


db = SQLAlchemy(app)

###########################
# Authentication
###########################


###########################
# Blueprints
###########################

from app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

# with app.app_context():
#     db.create_all()