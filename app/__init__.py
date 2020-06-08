from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SECRET_KEY"] = "Secretsadiopfkaspdofk"
socketio = SocketIO(app)

from app import routes, sockets


