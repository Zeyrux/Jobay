from .models import create_user_db, User

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email_address import validate_email


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if not email:
            flash("Bitte Email eingeben!", category="error")
        elif not password:
            flash("Bitte Password eingeben!", category="error")
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash(
                        "Flasches Passwort oder flasche Email addresse!",
                        category="error",
                    )
            else:
                flash("Email nicht registriert!", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email", "")
        first_name = request.form.get("first_name", "")
        last_name = request.form.get("last_name", "")
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        post_code = request.form.get("post_code", "")
        city = request.form.get("city", "")

        if not email:
            flash("Bitte Email angeben!", category="error")
        elif User.query.filter_by(email=email).first():
            flash("Email ist schon registriert!", category="error")
        elif not first_name:
            flash("Bitte Vorname(n) angeben!", category="error")
        elif not last_name:
            flash("Bitte Nachname angeben!", category="error")
        elif not password:
            flash("Bitte Password angeben!", category="error")
        elif not password_confirm:
            flash("Bitte Password bestätigen!", category="error")
        elif not post_code:
            flash("Bitte Postleitzahl eingeben!", category="error")
        elif not city:
            flash("Bitte Stadt angeben!", category="error")
        elif not validate_email(email):
            flash("Bitte existierende Email angeben!", category="error")
        elif len(first_name) <= 1:
            flash(
                "Bitte Vorname mit mehr als einem Buchstaben eingeben!",
                category="error",
            )
        elif len(last_name) <= 1:
            flash(
                "Bitte Nachname mit mehr als einem Buchstaben eingeben!",
                category="error",
            )
        elif len(password) < 8:
            flash(
                "Bitte ein Password mit mindestens 8 Zeichen wählen!", category="error"
            )
        elif password != password_confirm:
            flash("Passwörter stimmen nicht überein!", category="error")
        elif not post_code.replace("-", "").isdigit():
            flash(
                "Postleitzahl muss aus Zahlen und/oder Bindestrichen bestehen!",
                category="error",
            )
        else:
            user = create_user_db(
                email,
                first_name,
                last_name,
                generate_password_hash(password, method="sha256"),
                post_code,
                city,
            )
            flash("Profil Erstellt!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)
