from json import load
from pathlib import Path
from secrets import token_urlsafe

from flask_socketio import SocketIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
app = Flask(__name__)
mail = Mail(app)
socket = SocketIO(app)
online_users = {}


def get_app_config() -> None:
    db_credentials = load(
        open(Path("website", "db_credentials", "db_credentials.json"), "r")
    )
    return {
        "SECRET_KEY": token_urlsafe(25),
        "db_uri": (
            f"mysql+pymysql://{db_credentials['username']}:{db_credentials['password']}"
            + f"@{db_credentials['location']}:{db_credentials['port']}/"
            + f"{db_credentials['db_name']}"
        ),
        "profile_img_dir": Path("static", "images", "profile"),
        "job_img_dir": Path("static", "images", "job"),
        "website_profile_img_dir": Path("website", "static", "images", "profile"),
        "website_job_img_dir": Path("website", "static", "images", "job"),
        "profile_img_default": Path("static", "images", "profile", "default.png"),
        "job_img_default": Path("static", "images", "job", "default.png"),
    }


def create_app():
    # app
    app.config.update(get_app_config())  # TODO: Remove from here on
    app.config["SECRET_KEY"] = token_urlsafe(25)
    app.config["UPLOAD_FOLDER_PROFILE_IMAGE"] = Path("static", "images", "profile")
    app.config["UPLOAD_FOLDER_JOB_IMAGE"] = Path("static", "images", "job")
    app.config["UPLOAD_FOLDER_PROFILE_IMAGE_WEBSITE"] = Path(
        "website", "static", "images", "profile"
    )
    app.config["PROFILE_IMAGE_EMPTY"] = Path(
        app.config["UPLOAD_FOLDER_PROFILE_IMAGE"], "default.png"
    )
    app.config["JOB_IMAGE_EMPTY"] = Path(
        app.config["UPLOAD_FOLDER_JOB_IMAGE"], "default.png"
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
    from .routes import views
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
        from .models import Tag

        app.config["TAGS"] = [tag.name for tag in Tag.query.all()]
        # TODO: TAGS bei profile page überarbeite (von js in html)

    return app, socket


def create_database(app: Flask):
    if len(db.engine.table_names()) == 0:
        db.create_all()
        print("Created Database!")
    fill_db()
    print("Filled Database!")


def fill_db():
    from .init_db import init_db

    init_db(db)
