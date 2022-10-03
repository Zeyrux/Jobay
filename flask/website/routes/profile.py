from json import dumps
from pathlib import Path
from datetime import datetime

from .. import db
from ..models import (
    User,
    Tag,
    create_city,
    create_location,
    create_timeblock,
)

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    current_app,
    send_file,
)
from validate_email_address import validate_email
from flask_login import current_user, login_required

profile_bp = Blueprint("profile", __name__)
ALLOWED_FILE_EXTENSIONS = ["jpg", "jpeg", "png", "ico"]


@profile_bp.route("/profile-image", methods=["GET"])
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


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    path_image_profile = Path(
        current_app.config["UPLOAD_FOLDER_PROFILE_IMAGE_WEBSITE"],
        f"{current_user.id}.png",
    )
    if request.method == "POST":
        # email
        if "email" in request.form:
            if validate_email(request.form["email"]):
                if User.query.filter_by(email=request.form["email"]).first():
                    flash("Email ist schon registriert!", category="error")
                else:
                    current_user.email = request.form["email"]
                    db.session.commit()
            else:
                flash("Bitte existierende Email angeben!", category="error")
        # name
        elif "name" in request.form:
            if " " in request.form["name"]:
                first_name, last_name = request.form["name"].rsplit(" ", 1)
                current_user.first_name = first_name
                current_user.last_name = last_name
                db.session.commit()
            else:
                flash(
                    "Bitte Vor- und Nachname eingeben und mit einem Leerzeichen trennen!",
                    category="error",
                )
        # location
        elif "location" in request.form:
            if " " in request.form["location"]:
                post_code, city = request.form["location"].split(" ", 1)
                if not post_code.replace("-", "").isdigit():
                    flash(
                        "Postleitzahl muss aus Zahlen und/oder Bindestrichen bestehen!",
                        category="error",
                    )
                else:
                    city = create_city(city)
                    location = create_location(post_code, city)
                    current_user.location = location
                    db.session.commit()
            else:
                flash(
                    "Bitte Postleitzahl und Stadt mit einem Leerzeichen trennen!",
                    category="error",
                )
        # tags
        elif "add_tag" in request.form:
            tag = request.form.get("add_tag", "")
            if not tag:
                flash("Bitte Tag angeben!", category="error")
            elif not tag in current_app.config["TAGS"]:
                flash("Tag existiert nicht!", category="error")
            else:
                tag = Tag.query.filter_by(name=tag).first()
                if tag in current_user.tags:
                    flash("Du besitzt diesen Tag bereits", category="error")
                else:
                    current_user.tags.append(tag)
                    db.session.commit()
        # remove tags
        elif "remove_tag" in request.form:
            tag = request.form.get("remove_tag", "")
            if not tag:
                flash("Tag konnte nicht ausgelesen werden!", category="error")
            elif not tag in current_app.config["TAGS"]:
                flash("Tag existiert nicht!", category="error")
            else:
                tag = Tag.query.filter_by(name=tag).first()
                if tag in current_user.tags:
                    current_user.tags.remove(tag)
                    db.session.commit()
        # description
        elif "description" in request.form:
            if len(request.form["description"]) > 2048:
                flash(
                    "Bitte eine Beschreibung mit weniger als 2048 Zeichen eingeben!",
                    category="error",
                )
            else:
                current_user.description = request.form["description"]
                db.session.commit()
        # timeblock
        elif "day" in request.form:
            start = request.form.get("start", "")
            end = request.form.get("end", "")
            day = request.form.get("day", "")
            if not start:
                flash("Bitte Start Zeit angeben!", category="error")
            elif not end:
                flash("Bitte Endzeit angeben!", category="error")
            elif (
                not day
                or not ":" in start
                or not ":" in end
                or not len(day) == 1
                or not day.isdigit()
            ):
                flash(
                    "Fehler: Daten konnten nicht ausgelesen werden. Bitte versuchen Sie es erneut!",
                    category="error",
                )
            elif (
                not 0 < int(day) < 8
                or not start.split(":")[0].isdigit()
                or not end.split(":")[1].isdigit()
            ):
                flash(
                    "Fehler: Daten konnten nicht ausgelesen werden. Bitte versuchen Sie es erneut!",
                    category="error",
                )
            else:
                current_user.timeblocks.append(
                    create_timeblock(int(day), start, int(day), end)
                )
                db.session.commit()
        # delete timeblock
        elif "delete_timeblock" in request.form:
            timeblock = request.form.get("delete_timeblock", "")
            day = request.form.get("timeblock_delete_day", "")
            if not timeblock:
                flash("Bitte einen Zeitblock angeben!", category="error")
            elif not (";" in timeblock and timeblock.count(":") == 2 and day):
                flash(
                    "Fehler bei der Datenübertragung. Bitte erneut versuche!",
                    category="error",
                )
            elif not (
                ("".join(("".join(timeblock.split(";"))).split(":"))).isdigit()
                and day.isdigit()
            ):
                flash(
                    "Fehler bei der Datenübertragung. Bitte erneut versuche!",
                    category="error",
                )
            else:
                timeblock = current_user.timeblocks.filter_by(
                    start=datetime(
                        2000,
                        1,
                        int(day),
                        int(timeblock.split(";")[0].split(":")[0]),
                        int(timeblock.split(";")[0].split(":")[1]),
                    ).timestamp(),
                    end=datetime(
                        2000,
                        1,
                        int(day),
                        int(timeblock.split(";")[1].split(":")[0]),
                        int(timeblock.split(";")[1].split(":")[1]),
                    ).timestamp(),
                ).first()
                if timeblock:
                    current_user.timeblocks.remove(timeblock)
                    db.session.commit()
        # profile image
        elif "profile_image" in request.files:
            image = request.files["profile_image"]
            if not image.filename:
                flash("Bitte Bild auswählen!", category="error")
            elif not (
                "." in image.filename
                and image.filename.rsplit(".", 1)[1] in ALLOWED_FILE_EXTENSIONS
            ):
                flash("Fehler beim Dateinamen!", category="error")
            else:
                if path_image_profile.exists():
                    path_image_profile.unlink()
                image.save(path_image_profile)
                flash("Profilbild gespeichern!", category="success")
    return render_template(
        "profile.html",
        user=current_user,
        timeblocks=dumps(
            [timeblock.to_dict() for timeblock in current_user.timeblocks]
        ),
        user_tags=dumps([tag.to_dict() for tag in current_user.tags]),
        all_tags=dumps(current_app.config["TAGS"]),
    )
