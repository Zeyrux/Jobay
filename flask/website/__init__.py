from pathlib import Path
from secrets import token_urlsafe

from flask_socketio import SocketIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_urlsafe(25)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    # routes
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # database
    from .models import User

    create_database(app)

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, SocketIO(app)


def create_database(app):
    if not Path("website", DB_NAME).exists():
        db.create_all(app=app)
        print("Created Database!")
