from json import load
from pathlib import Path
from secrets import token_urlsafe

from flask_socketio import SocketIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    # app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_urlsafe(25)
    app.config["UPLOAD_FOLDER_PROFILE_IMAGE"] = Path("static", "images")
    app.config["UPLOAD_FOLDER_PROFILE_IMAGE_WEBSITE"] = Path(
        "website", "static", "images"
    )
    db_credentials = load(
        open(Path("website", "db_credentials", "db_credentials.json"), "r")
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_credentials['username']}:{db_credentials['password']}"
        + f"@{db_credentials['location']}:{db_credentials['port']}/"
        + f"{db_credentials['db_name']}"
    )

    # routes
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # database
    from .models import User

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Um diese Seite zu nutzen musst du dich einloggen"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.before_first_request
    def init_app():
        create_database(app)

    return app, SocketIO(app)


def create_database(app: Flask):
    if len(db.engine.table_names()) == 0:
        db.create_all(app=app)
        print("Created Database!")
        fill_db()
        print("Filled Database!")


def fill_db():
    from .init_db import init_db

    init_db(db)
