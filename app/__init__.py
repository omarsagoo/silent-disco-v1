

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from app.config import Config
from flask_login import LoginManager, login_manager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

socketio = SocketIO(app)


db = SQLAlchemy(app)

from .models import User
###########################
# Authentication
###########################
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


bcrypt = Bcrypt(app)

###########################
# Blueprints
###########################

from app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

# with app.app_context():
#     db.create_all()
