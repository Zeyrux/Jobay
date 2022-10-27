from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("chat", methods=["GET", "POST"])
@login_required
def chat():
    request.args.get("id", "")
    id = request.args.get("id", "")
    if not id or not id.isdigit():
        flash("Job nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
