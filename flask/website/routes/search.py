from ..models import User, Job
from .base import generate_args_base_template

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user

search_bp = Blueprint("search", __name__)


def get_search_jobs(user: User, search: str) -> list[Job]:
    return Job.query.filter_by(Job.name.contains(search))


@search_bp.route("/search", methods=["GET"])
@login_required
def search():
    return render_template("search.html" ** generate_args_base_template(current_user))
