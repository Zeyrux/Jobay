from json import dumps
from pathlib import Path
from datetime import datetime

from . import db
from .models import (
    User,
    create_job_db,
    create_city,
    create_location,
    create_timeblock,
)

from validate_email_address import validate_email
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_file,
    send_from_directory,
    current_app,
)
from flask_login import login_required, current_user


views = Blueprint("views", __name__)
ALLOWED_FILE_EXTENSIONS = ["jpg", "jpeg", "png", "ico"]


def str_to_datetime(string: str) -> datetime | None:
    try:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None


@views.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        Path("images"), "favicon.ico", mimetype="image/vnd.microsoft.ico"
    )


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/profile", methods=["GET", "POST"])
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
        # description
        # check lenght of description (maybe to long)
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
    )


@views.route("/profile-image", methods=["GET"])
@login_required
def profile_image():
    return send_file(
        Path(
            current_app.config["UPLOAD_FOLDER_PROFILE_IMAGE"],
            f"{current_user.id}.png",
        )
    )


@views.route("/create-job", methods=["GET", "POST"])
@login_required
def create_job():
    if request.method == "POST":
        name = request.form.get("name", "")
        duration_hour = request.form.get("duration_hour", "")
        duration_minute = request.form.get("duration_minute", "")
        time_start = str_to_datetime(request.form.get("time_start", ""))
        payment_euro = request.form.get("payment_euro", "")
        payment_cent = request.form.get("payment_cent", "")
        post_code = request.form.get("post_code", "")
        city = request.form.get("city", "")
        if not name:
            flash("Bitte Name des Jobs einfügen!", category="error")
        elif not duration_hour and not duration_minute:
            flash("Bitte die Dauer eingeben!", category="error")
        elif not time_start:
            flash("Bitte die Start Zeit eingeben!", category="error")
        elif not payment_euro and not payment_cent:
            flash("Bitte eine Bezahlung eingeben!", category="error")
        elif not post_code:
            flash("Bitte eine Postleitzahl eingeben!", category="error")
        elif not city:
            flash("Bitte eine Stadt eingeben!", category="error")
        elif not duration_minute.isdigit() or not duration_hour.isdigit():
            flash("Bitte die Dauer in Zahlen angeben!", category="error")
        elif not payment_euro.isdigit() or not payment_cent.isdigit():
            flash("Bitte die Bezahlung in Zahlen angeben!", category="error")
        elif not post_code.replace("-", "").isdigit():
            flash(
                "Postleitzahl muss aus Zahlen und/oder Bindestrichen bestehen!",
                category="error",
            )
        else:
            create_job_db(
                current_user,
                name,
                int(duration_hour) * 60 + int(duration_minute),
                int(time_start.timestamp()),
                int(payment_euro) * 100 + int(payment_cent),
                post_code,
                city,
            )
            flash("Job erstellt", category="success")
            return redirect(url_for("views.home"))
    return render_template("create_job.html", user=current_user)
