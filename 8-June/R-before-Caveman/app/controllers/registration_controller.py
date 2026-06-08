from collections import OrderedDict

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.repositories import course_repository
from app.repositories import registration_repository
from app.repositories import student_repository
from app.utils.decorators import login_required
from app.utils.validators import validate_registration_form


registrations_bp = Blueprint("registrations", __name__, url_prefix="/registrations")


@registrations_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_registrations():
    students = student_repository.list_students()
    courses = course_repository.list_courses()
    errors = {}
    form_data = {"student_id": "", "course_ids": []}

    if request.method == "POST":
        form_data, errors = validate_registration_form(
            {
                "student_id": request.form.get("student_id"),
                "course_ids": request.form.getlist("course_ids"),
            }
        )

        student = student_repository.get_student(form_data["student_id"]) if not errors.get("student_id") else None
        if student is None and not errors.get("student_id"):
            errors["student_id"] = "Selected student does not exist."

        existing_course_ids = course_repository.fetch_existing_course_ids(form_data["course_ids"])
        missing_course_ids = sorted(set(form_data["course_ids"]) - existing_course_ids)
        if missing_course_ids:
            errors["course_ids"] = "One or more selected courses are no longer available."

        if not errors:
            result = registration_repository.create_registrations(form_data["student_id"], form_data["course_ids"])
            if result["created_count"] == 0:
                flash("No new registrations were created because those course selections already exist.", "info")
            else:
                flash(f"{result['created_count']} course registration(s) saved successfully.", "success")
                if result["duplicate_course_ids"]:
                    flash("Duplicate course selections were skipped automatically.", "warning")
            return redirect(url_for("registrations.manage_registrations"))

        flash("Please fix the registration form errors.", "danger")

    registration_cards = _build_registration_cards()
    return render_template(
        "registrations/list.html",
        students=students,
        courses=courses,
        form_data=form_data,
        errors=errors,
        registration_cards=registration_cards,
    )


@registrations_bp.route("/<int:registration_id>/delete", methods=["POST"])
@login_required
def delete_registration(registration_id):
    registration = registration_repository.get_registration(registration_id)
    if registration is None:
        abort(404)

    registration_repository.delete_registration(registration_id)
    flash("Registration removed successfully.", "success")
    return redirect(url_for("registrations.manage_registrations"))


def _build_registration_cards():
    overview_rows = registration_repository.get_student_registration_overview()
    students = OrderedDict()

    for row in overview_rows:
        student_id = row["student_id"]
        if student_id not in students:
            students[student_id] = {
                "student_id": student_id,
                "full_name": row["full_name"],
                "enrollment_number": row["enrollment_number"],
                "department": row["department"],
                "year": row["year"],
                "courses": [],
            }

        if row["course_id"] is not None:
            students[student_id]["courses"].append(
                {
                    "registration_id": row["registration_id"],
                    "course_id": row["course_id"],
                    "label": f"{row['course_code']} - {row['title']}",
                }
            )

    return list(students.values())
