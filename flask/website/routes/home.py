from datetime import datetime
from json import dumps

from ..models import Job, User, user_tag, job_tag
from .. import db, socket
from .base import generate_args_base_template

from flask import render_template, Blueprint, request, flash
from flask_login import login_required, current_user


home_bp = Blueprint("home", __name__)


def get_jobs_for_user(user: User) -> list[Job]:
    return Job.query.all()


def get_search_jobs(user: User, search: str) -> list[Job]:
    jobs = Job.query.all()
    result = []
    for job in jobs:
        if str(search) in str(job.name):
            result.append(job)
    return result
    return Job.query.filter_by(Job.name.contains(search)).limit(10).all()


@home_bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    jobs = []
    if request.method == "POST":
        search = request.form.get("search", "")
        if not search:
            flash(
                "Bitte füge etwas in die Suche ein um dannach zu filtern",
                category="error",
            )
            print("not there")
        else:
            jobs = get_search_jobs(current_user, search)
    if len(jobs) == 0:
        jobs = get_jobs_for_user(current_user)
    return render_template(
        "home.html",
        **generate_args_base_template(current_user),
        jobs=dumps([job.to_dict(short=True) for job in jobs]),
        datetime=datetime,
        int=int,
        str=str,
    )


@socket.on("request_jobs")
def request_jobs():
    socket.emit(
        "answer_request_jobs",
        dumps([job.to_dict(short=True) for job in get_jobs_for_user(current_user)]),
    )
