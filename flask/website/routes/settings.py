from .. import socket, db

from flask import Blueprint, render_template
from flask_login import login_required


settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("settings.html")