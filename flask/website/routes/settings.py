from .base import generate_args_base_template

from flask import Blueprint, render_template
from flask_login import login_required, current_user


settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template(
        "settings.html", **generate_args_base_template(current_user), user=current_user
    )
