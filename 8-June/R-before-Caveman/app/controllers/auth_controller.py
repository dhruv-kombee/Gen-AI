from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.auth_service import validate_admin_credentials


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("dashboard.home"))

    error_message = None
    entered_username = ""

    if request.method == "POST":
        entered_username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not entered_username or not password:
            error_message = "Please enter both username and password."
        elif validate_admin_credentials(entered_username, password):
            session.clear()
            session["admin_logged_in"] = True
            session["admin_username"] = entered_username
            session.permanent = True
            flash("Welcome back. You are now logged in.", "success")
            return redirect(url_for("dashboard.home"))
        else:
            error_message = "Invalid admin credentials."

    return render_template("login.html", error_message=error_message, entered_username=entered_username)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))
