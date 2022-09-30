from pathlib import Path

from .profile import profile
from .create_job import create_job

from flask import (
    Blueprint,
    send_from_directory,
    render_template,
)
from flask_login import login_required, current_user


views = Blueprint("views", __name__)
views.register_blueprint(profile, url_prefix="/")
views.register_blueprint(create_job, url_prefix="/")


@views.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        Path("images"), "favicon.ico", mimetype="image/vnd.microsoft.ico"
    )


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)
