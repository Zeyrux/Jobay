from datetime import datetime

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


def str_to_datetime(string: str) -> datetime | None:
    try:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)


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
        print(time_start)
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
            pass

    return render_template("create_job.html", user=current_user)