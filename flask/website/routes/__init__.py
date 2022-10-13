from pathlib import Path

from .profile import profile_bp
from .create_job import create_job_bp
from .home import home_bp
from .job import job_bp
from .view_profile import view_profile_bp
from .settings import settings_bp

from flask import (
    Blueprint,
    send_from_directory,
)


views = Blueprint("views", __name__)
views.register_blueprint(profile_bp, url_prefix="/")
views.register_blueprint(create_job_bp, url_prefix="/")
views.register_blueprint(home_bp, url_prefix="/")
views.register_blueprint(job_bp, url_prefix="/")
views.register_blueprint(view_profile_bp, url_prefix="/")
views.register_blueprint(settings_bp, url_prefix="/")


@views.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        Path("images"), "favicon.ico", mimetype="image/vnd.microsoft.ico"
    )
