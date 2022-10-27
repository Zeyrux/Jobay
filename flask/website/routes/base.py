from pathlib import Path

from ..models import User

from flask import Blueprint, request, flash, send_file, current_app, send_from_directory
from flask_login import login_required, current_user


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
    print(unread_chats)
    return {"unread_chats": unread_chats}


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
