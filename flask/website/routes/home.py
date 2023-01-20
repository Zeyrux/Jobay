from datetime import datetime
from json import dumps

from ..models import Job, User, user_tag, job_tag
from .. import db, socket
from .base import generate_args_base_template

from flask import render_template, Blueprint
from flask_login import login_required, current_user


home_bp = Blueprint("home", __name__)


def get_jobs_for_user(user: User) -> list[Job]:
    return Job.query.all()


@home_bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    jobs = get_jobs_for_user(current_user)
    return render_template(
        "home.html",
        **generate_args_base_template(current_user),
        jobs=jobs,
        datetime=datetime,
        int=int,
        str=str,
    )


@socket.on("search")
def search(search):
    print(search)
    socket.emit(dumps([job.to_dict() for job in get_jobs_for_user(current_user)]))
