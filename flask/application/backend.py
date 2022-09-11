import secrets

from Database import ConnectionDB

from flask import Flask, render_template, session
from flask_socketio import SocketIO


class App:

    connected = False
    scanning = False

    def __init__(self) -> None:
        # app
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_urlsafe(16)
        self.socket = SocketIO(self.app)

        self.register_routes()

    def register_routes(self):
        @self.app.route("/")
        def homepage():
            session["database"] = ConnectionDB()
            return render_template("homepage.html")
