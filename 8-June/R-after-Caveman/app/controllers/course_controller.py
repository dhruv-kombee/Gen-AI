import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models.course_model import create_course, delete_course, get_course, list_courses, update_course
from app.utils.decorators import login_required
from app.utils.validators import parse_course_integrity_error, validate_course_payload

course_bp = Blueprint("courses", __name__, url_prefix="/courses")


@course_bp.route("/")
@login_required
def index():
    courses = list_courses()
    return render_template("courses/index.html", courses=courses)


@course_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors, cleaned_data = validate_course_payload(form_data)
        if not errors:
            try:
                create_course(cleaned_data)
                flash("Course added successfully.", "success")
                return redirect(url_for("courses.index"))
            except sqlite3.IntegrityError as exc:
                errors = parse_course_integrity_error(str(exc))

    return render_template(
        "courses/form.html",
        errors=errors,
        form_action=url_for("courses.create"),
        form_data=form_data,
        page_title="Add Course",
        submit_label="Save Course",
    )


@course_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def edit(course_id):
    course = get_course(course_id)
    if course is None:
        flash("Course record not found.", "danger")
        return redirect(url_for("courses.index"))

    errors = {}
    form_data = dict(course)

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors, cleaned_data = validate_course_payload(form_data)
        if not errors:
            try:
                update_course(course_id, cleaned_data)
                flash("Course updated successfully.", "success")
                return redirect(url_for("courses.index"))
            except sqlite3.IntegrityError as exc:
                errors = parse_course_integrity_error(str(exc))

    return render_template(
        "courses/form.html",
        errors=errors,
        form_action=url_for("courses.edit", course_id=course_id),
        form_data=form_data,
        page_title="Edit Course",
        submit_label="Update Course",
    )


@course_bp.route("/<int:course_id>/delete", methods=["POST"])
@login_required
def delete(course_id):
    course = get_course(course_id)
    if course is None:
        flash("Course record not found.", "danger")
    else:
        delete_course(course_id)
        flash(f"{course['course_code']} was deleted.", "info")
    return redirect(url_for("courses.index"))

