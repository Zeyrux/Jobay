from datetime import datetime
from pathlib import Path
from json import dumps

from .. import socket, db, online_users
from ..models import User, Message

from flask import Blueprint, request, flash, send_file, current_app, send_from_directory
from flask_login import login_required, current_user
from flask_socketio import emit


base_bp = Blueprint("base", __name__)


def generate_args_base_template(user) -> dict:
    unread_msgs = user.messages_receive.filter_by(received=False).all()
    unread_chats = {}
    for msg in unread_msgs:
        if unread_chats.get(msg.id_user_send):
            unread_chats[msg.id_user_send]["messages"].append(msg.to_dict())
        else:
            user = User.query.filter_by(id=msg.id_user_send).first()
            unread_chats[msg.id_user_send] = {
                "user_first_name": user.first_name,
                "user_last_name": user.last_name,
                "messages": [msg.to_dict()],
            }
    return {"unread_chats": unread_chats, "user": user}


def get_chat(
    user_first_id: User, user_second_id: User
) -> tuple[list[Message], list[Message]]:
    msgs_first = Message.query.filter_by(
        id_user_send=user_first_id, id_user_receive=user_second_id
    ).all()
    msgs_second = Message.query.filter_by(
        id_user_send=user_second_id, id_user_receive=user_first_id
    ).all()
    return [msg.to_dict() for msg in msgs_first], [msg.to_dict() for msg in msgs_second]


@base_bp.route("/profile-image", methods=["GET"])
@login_required
def profile_image():
    user_id = request.args.get("user_id", "")
    if user_id:
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            flash("Fehler bei der Benutzer ID!", category="error")
            return send_file(current_app.config["PROFILE_IMAGE_EMPTY"])
    else:
        user_id = current_user.id
    if Path(
        current_app.config["UPLOAD_FOLDER_PROFILE_IMAGE_WEBSITE"],
        f"{user_id}.png",
    ).exists():
        return send_file(
            Path(
                current_app.config["UPLOAD_FOLDER_PROFILE_IMAGE"],
                f"{user_id}.png",
            )
        )
    return send_file(current_app.config["PROFILE_IMAGE_EMPTY"])


@base_bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        Path("images"), "favicon.ico", mimetype="image/vnd.microsoft.ico"
    )


@socket.on("msg_send")
def msg_send(msg, chat_partner_id):
    if 0 < len(msg) < 2048 and chat_partner_id.isdigit():
        chat_partner = User.query.filter_by(id=int(chat_partner_id)).first()
        if chat_partner:
            msg_db = Message(
                content=msg,
                time=int(datetime.now().timestamp() * 100),
                id_user_send=current_user.id,
                id_user_receive=chat_partner.id,
            )
            employer_sid = online_users.get(chat_partner.id, False)
            if employer_sid:
                emit("receive_msg", msg_db.to_dict(), room=employer_sid)
            db.session.add(msg_db)
            db.session.commit()
        else:
            flash("Fehler bei der Suche des Gesprächspartners!", category="error")
