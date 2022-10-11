from json import dumps

from ..models import User
from .. import online_users

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


view_profile_bp = Blueprint("view_profile", __name__)


@view_profile_bp.route("/view-profile", methods=["GET"])
@login_required
def view_profile():
    id = request.args.get("id", "")
    if not id or not id.isdigit():
        flash("Profile nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
    profile = User.query.filter_by(id=id).first()
    if not profile:
        flash("Profile nicht gefunden!", category="error")
        return redirect(url_for("views.home.home"))
    online = profile.id in online_users
    return render_template(
        "view_profile.html",
        user=current_user,
        profile=profile,
        online=online,
        profile_tags=dumps([tag.to_dict() for tag in profile.tags]),
    )
