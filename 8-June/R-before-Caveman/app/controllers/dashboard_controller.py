from flask import Blueprint, render_template

from app.repositories.course_repository import count_courses
from app.repositories.registration_repository import count_registrations
from app.repositories.registration_repository import get_recent_registrations
from app.repositories.student_repository import count_students
from app.utils.decorators import login_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def home():
    stats = {
        "students": count_students(),
        "courses": count_courses(),
        "registrations": count_registrations(),
    }
    recent_registrations = get_recent_registrations(limit=6)
    return render_template("dashboard.html", stats=stats, recent_registrations=recent_registrations)
