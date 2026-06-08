from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.repositories import course_repository
from app.utils.constants import DEPARTMENTS
from app.utils.decorators import login_required
from app.utils.validators import validate_course_form


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
@login_required
def list_courses():
    courses = course_repository.list_courses()
    return render_template("courses/list.html", courses=courses)


@courses_bp.route("/add", methods=["GET", "POST"])
@login_required
def create_course():
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data, errors = validate_course_form(request.form)

        if course_repository.course_code_exists(form_data["course_code"]):
            errors["course_code"] = "This course code is already in use."

        if not errors:
            course_repository.create_course(form_data)
            flash("Course added successfully.", "success")
            return redirect(url_for("courses.list_courses"))

        flash("Please correct the highlighted course details.", "danger")

    return render_template(
        "courses/form.html",
        page_title="Add Course",
        form_action=url_for("courses.create_course"),
        form_data=form_data,
        errors=errors,
        departments=DEPARTMENTS,
        submit_label="Create Course",
    )


@courses_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    course = course_repository.get_course(course_id)
    if course is None:
        abort(404)

    errors = {}
    form_data = course

    if request.method == "POST":
        form_data, errors = validate_course_form(request.form)

        if course_repository.course_code_exists(form_data["course_code"], exclude_course_id=course_id):
            errors["course_code"] = "This course code is already in use."

        if not errors:
            course_repository.update_course(course_id, form_data)
            flash("Course updated successfully.", "success")
            return redirect(url_for("courses.list_courses"))

        flash("Please correct the highlighted course details.", "danger")

    return render_template(
        "courses/form.html",
        page_title="Edit Course",
        form_action=url_for("courses.edit_course", course_id=course_id),
        form_data=form_data,
        errors=errors,
        departments=DEPARTMENTS,
        submit_label="Update Course",
    )


@courses_bp.route("/<int:course_id>/delete", methods=["POST"])
@login_required
def delete_course(course_id):
    course = course_repository.get_course(course_id)
    if course is None:
        abort(404)

    course_repository.delete_course(course_id)
    flash("Course deleted successfully.", "success")
    return redirect(url_for("courses.list_courses"))
