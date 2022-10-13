from datetime import datetime

from ..models import Job, User, user_tag, job_tag
from .. import db

from flask import render_template, Blueprint
from flask_login import login_required, current_user


home_bp = Blueprint("home", __name__)


def get_jobs_for_user(user: User):
    return Job.query.all()


@home_bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    jobs = get_jobs_for_user(current_user)
    return render_template(
        "home.html",
        user=current_user,
        jobs=jobs,
        datetime=datetime,
        int=int,
        str=str,
    )
