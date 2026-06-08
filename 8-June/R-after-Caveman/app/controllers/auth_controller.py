from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.models.auth_model import get_admin_by_username
from app.utils.validators import validate_login_payload

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("dashboard.index"))

    errors = {}

    if request.method == "POST":
        payload = {
            "username": request.form.get("username", ""),
            "password": request.form.get("password", ""),
        }
        errors, cleaned_data = validate_login_payload(payload)

        if not errors:
            admin = get_admin_by_username(cleaned_data["username"])
            if admin and check_password_hash(admin["password_hash"], cleaned_data["password"]):
                session.clear()
                session["admin_id"] = admin["id"]
                session["admin_username"] = admin["username"]
                flash("Welcome back. You are now signed in.", "success")
                return redirect(url_for("dashboard.index"))

            errors["general"] = "Invalid username or password."

    return render_template("auth/login.html", errors=errors)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

