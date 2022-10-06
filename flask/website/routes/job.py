from datetime import datetime
from collections import namedtuple
from itertools import count

from ..models import Job, Message
from .. import db

from flask import Blueprint, request, flash, redirect, render_template, url_for
from flask_login import login_required, current_user


UserMessage = namedtuple("Message", ["send", "receive"])
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
    msgs_send = Message.query.filter_by(
        id_user_send=current_user.id, id_user_receive=job.employer.id
    ).all()
    msgs_receive = Message.query.filter_by(
        id_user_send=job.employer.id, id_user_receive=current_user.id
    ).all()
    return render_template(
        "job.html",
        user=current_user,
        job=job,
        datetime=datetime,
        count=count,
        msgs=UserMessage(msgs_send, msgs_receive),
        cnt_msgs=len(msgs_send) + len(msgs_receive),
    )
