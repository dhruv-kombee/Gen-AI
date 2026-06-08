from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.repositories import student_repository
from app.utils.constants import ACADEMIC_YEARS, DEPARTMENTS
from app.utils.decorators import login_required
from app.utils.validators import validate_student_form


students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
@login_required
def list_students():
    search_term = (request.args.get("search") or "").strip()
    students = student_repository.list_students(search_term=search_term)
    return render_template("students/list.html", students=students, search_term=search_term)


@students_bp.route("/add", methods=["GET", "POST"])
@login_required
def create_student():
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data, errors = validate_student_form(request.form)

        if student_repository.enrollment_exists(form_data["enrollment_number"]):
            errors["enrollment_number"] = "This enrollment number is already in use."

        if student_repository.email_exists(form_data["email"]):
            errors["email"] = "This email address is already in use."

        if not errors:
            student_repository.create_student(form_data)
            flash("Student added successfully.", "success")
            return redirect(url_for("students.list_students"))

        flash("Please correct the highlighted student details.", "danger")

    return render_template(
        "students/form.html",
        page_title="Add Student",
        form_action=url_for("students.create_student"),
        form_data=form_data,
        errors=errors,
        departments=DEPARTMENTS,
        academic_years=ACADEMIC_YEARS,
        submit_label="Create Student",
    )


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = student_repository.get_student(student_id)
    if student is None:
        abort(404)

    errors = {}
    form_data = student

    if request.method == "POST":
        form_data, errors = validate_student_form(request.form)

        if student_repository.enrollment_exists(form_data["enrollment_number"], exclude_student_id=student_id):
            errors["enrollment_number"] = "This enrollment number is already in use."

        if student_repository.email_exists(form_data["email"], exclude_student_id=student_id):
            errors["email"] = "This email address is already in use."

        if not errors:
            student_repository.update_student(student_id, form_data)
            flash("Student updated successfully.", "success")
            return redirect(url_for("students.list_students"))

        flash("Please correct the highlighted student details.", "danger")

    return render_template(
        "students/form.html",
        page_title="Edit Student",
        form_action=url_for("students.edit_student", student_id=student_id),
        form_data=form_data,
        errors=errors,
        departments=DEPARTMENTS,
        academic_years=ACADEMIC_YEARS,
        submit_label="Update Student",
    )


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    student = student_repository.get_student(student_id)
    if student is None:
        abort(404)

    student_repository.delete_student(student_id)
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students.list_students"))
