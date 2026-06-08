import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models.student_model import create_student, delete_student, get_student, list_students, update_student
from app.utils.decorators import login_required
from app.utils.validators import parse_student_integrity_error, validate_student_payload

student_bp = Blueprint("students", __name__, url_prefix="/students")


@student_bp.route("/")
@login_required
def index():
    search = request.args.get("search", "").strip()
    students = list_students(search=search)
    return render_template("students/index.html", students=students, search=search)


@student_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors, cleaned_data = validate_student_payload(form_data)
        if not errors:
            try:
                create_student(cleaned_data)
                flash("Student added successfully.", "success")
                return redirect(url_for("students.index"))
            except sqlite3.IntegrityError as exc:
                errors = parse_student_integrity_error(str(exc))

    return render_template(
        "students/form.html",
        errors=errors,
        form_action=url_for("students.create"),
        form_data=form_data,
        page_title="Add Student",
        submit_label="Save Student",
    )


@student_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit(student_id):
    student = get_student(student_id)
    if student is None:
        flash("Student record not found.", "danger")
        return redirect(url_for("students.index"))

    errors = {}
    form_data = dict(student)

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors, cleaned_data = validate_student_payload(form_data)
        if not errors:
            try:
                update_student(student_id, cleaned_data)
                flash("Student updated successfully.", "success")
                return redirect(url_for("students.index"))
            except sqlite3.IntegrityError as exc:
                errors = parse_student_integrity_error(str(exc))

    return render_template(
        "students/form.html",
        errors=errors,
        form_action=url_for("students.edit", student_id=student_id),
        form_data=form_data,
        page_title="Edit Student",
        submit_label="Update Student",
    )


@student_bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def delete(student_id):
    student = get_student(student_id)
    if student is None:
        flash("Student record not found.", "danger")
    else:
        delete_student(student_id)
        flash(f"{student['full_name']} was deleted.", "info")
    return redirect(url_for("students.index"))

