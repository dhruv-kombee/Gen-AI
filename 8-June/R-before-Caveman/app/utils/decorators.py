from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("admin_logged_in"):
            return view(*args, **kwargs)

        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Authentication required."}), 401

        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    return wrapped_view
