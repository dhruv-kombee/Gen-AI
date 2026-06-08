from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models.course_model import list_course_choices
from app.models.registration_model import create_registrations, delete_registration, list_registrations
from app.models.student_model import list_student_choices
from app.utils.decorators import login_required
from app.utils.validators import validate_registration_payload

registration_bp = Blueprint("registrations", __name__, url_prefix="/registrations")


@registration_bp.route("/")
@login_required
def index():
    registrations = list_registrations()
    return render_template("registrations/index.html", registrations=registrations)


@registration_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    students = list_student_choices()
    courses = list_course_choices()
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict(flat=True)
        form_data["course_ids"] = request.form.getlist("course_ids")
        errors, cleaned_data = validate_registration_payload(form_data)

        if not errors:
            try:
                result = create_registrations(cleaned_data["student_id"], cleaned_data["course_ids"])
                duplicate_names = [row["course_code"] for row in result["duplicates"]]

                if result["created"]:
                    if duplicate_names:
                        flash(
                            f"Registration saved. Skipped duplicate courses: {', '.join(duplicate_names)}.",
                            "warning",
                        )
                    else:
                        flash("Courses registered successfully.", "success")
                    return redirect(url_for("registrations.index"))

                errors["course_ids"] = (
                    f"Selected courses already exist for this student: {', '.join(duplicate_names)}."
                    if duplicate_names
                    else "No new course registration was created."
                )
            except ValueError as exc:
                errors["course_ids"] = str(exc)

    return render_template(
        "registrations/form.html",
        students=students,
        courses=courses,
        errors=errors,
        form_data=form_data,
    )


@registration_bp.route("/<int:registration_id>/delete", methods=["POST"])
@login_required
def delete(registration_id):
    deleted = delete_registration(registration_id)
    if deleted:
        flash("Registration removed.", "info")
    else:
        flash("Registration record not found.", "danger")
    return redirect(url_for("registrations.index"))
