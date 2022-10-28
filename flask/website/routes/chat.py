from ..models import User
from .base import generate_args_base_template, get_chat

from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("chat", methods=["GET", "POST"])
@login_required
def chat():
    request.args.get("id", "")
    id = request.args.get("id", "")
    if not id or not id.isdigit():
        flash("Chat nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
    chat_partner = User.query.filter_by(id=id).first()
    if not chat_partner:
        flash("Chat Partner konnte nicht gefunden werden", category="error")
        return redirect(url_for("views.home.home"))
    msgs_send, msgs_receive = get_chat(current_user.id, chat_partner.id)
    return render_template(
        "chat.html",
        **generate_args_base_template(current_user),
        chat_partner=chat_partner,
        msgs_send=msgs_send,
        msgs_receive=msgs_receive
    )
