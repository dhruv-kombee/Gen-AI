from functools import wraps

from flask import jsonify, flash, redirect, request, session, url_for


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view_function(*args, **kwargs)

    return wrapped_view


def api_login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_id"):
            return jsonify({"success": False, "message": "Authentication required."}), 401
        return view_function(*args, **kwargs)

    return wrapped_view

