from datetime import datetime
from itertools import count

from ..models import Job
from .base import generate_args_base_template, get_chat

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
    job = Job.query.filter_by(id=id).first()
    if not job:
        flash("Job nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
    msgs_send, msgs_receive = get_chat(current_user.id, job.employer.id)
    return render_template(
        "job.html",
        **generate_args_base_template(current_user),
        job=job,
        msgs_send=msgs_send,
        msgs_receive=msgs_receive,
        cnt_msgs=len(msgs_send) + len(msgs_receive),
        datetime=datetime,
        count=count,
        len=len,
        str=str,
    )
