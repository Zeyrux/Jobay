from flask import Blueprint, request, flash, redirect, render_template, url_for
from flask_login import login_required, current_user


job_bp = Blueprint("job", __name__)


@job_bp.route("/job", methods=["GET"])
@login_required
def job():
    id = request.args.get("id", "")
    if not id or not id.isdigit():
        flash("Job nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
    return render_template("job.html", user=current_user)
