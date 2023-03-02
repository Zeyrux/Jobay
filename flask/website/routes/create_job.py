from datetime import datetime

from ..models import create_job_db
from .base import generate_args_base_template

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
)
from flask_login import current_user, login_required


create_job_bp = Blueprint("create_job", __name__)


def str_to_datetime(string: str) -> datetime | None:
    try:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None


@create_job_bp.route("/create-job", methods=["GET", "POST"])
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
        tags = [
            argument[1]
            for argument in request.form.items()
            if "tag_" in argument[0] and argument[1] in current_app.config["TAGS"]
        ][:2]
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
        elif not tags:
            flash("Bitte Tags eingeben!", category="error")
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
                tags,
            )
            flash("Job erstellt", category="success")
            return redirect(url_for("views.home.home"))
    return render_template(
        "create_job.html",
        **generate_args_base_template(current_user),
        tags=current_app.config["TAGS"]
    )
