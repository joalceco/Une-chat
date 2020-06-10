from flask import Flask, render_template
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
# app.config["SECRET_KEY"] = "Secretsadiopfkaspdofk"

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = "login"
socketio = SocketIO(app)

from app import routes, sockets


