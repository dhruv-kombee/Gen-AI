import sqlite3

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash

from app.models.auth_model import get_admin_by_username
from app.models.course_model import create_course, delete_course, get_course, list_course_choices, list_courses, update_course
from app.models.dashboard_model import get_dashboard_metrics
from app.models.registration_model import (
    create_registrations,
    delete_registration,
    get_registration,
    list_registrations,
)
from app.models.student_model import (
    create_student,
    delete_student,
    get_student,
    list_student_choices,
    list_students,
    update_student,
)
from app.utils.decorators import api_login_required
from app.utils.validators import (
    parse_course_integrity_error,
    parse_student_integrity_error,
    validate_course_payload,
    validate_login_payload,
    validate_registration_payload,
    validate_student_payload,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def make_response(success, message, data=None, status=200, errors=None):
    payload = {"success": success, "message": message}
    if data is not None:
        payload["data"] = data
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status


@api_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_login_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    admin = get_admin_by_username(cleaned_data["username"])
    if admin is None or not check_password_hash(admin["password_hash"], cleaned_data["password"]):
        return make_response(False, "Invalid username or password.", status=401)

    session.clear()
    session["admin_id"] = admin["id"]
    session["admin_username"] = admin["username"]
    return make_response(True, "Login successful.", data={"username": admin["username"]})


@api_bp.route("/logout", methods=["POST"])
@api_login_required
def logout():
    session.clear()
    return make_response(True, "Logout successful.")


@api_bp.route("/dashboard", methods=["GET"])
@api_login_required
def dashboard():
    metrics = get_dashboard_metrics()
    metrics["recent_registrations"] = [dict(row) for row in metrics["recent_registrations"]]
    return make_response(True, "Dashboard data loaded.", data=metrics)


@api_bp.route("/students", methods=["GET"])
@api_login_required
def get_students():
    search = request.args.get("search", "").strip()
    students = [dict(row) for row in list_students(search=search)]
    return make_response(True, "Students loaded.", data=students)


@api_bp.route("/students/<int:student_id>", methods=["GET"])
@api_login_required
def get_student_detail(student_id):
    student = get_student(student_id)
    if student is None:
        return make_response(False, "Student not found.", status=404)
    return make_response(True, "Student loaded.", data=dict(student))


@api_bp.route("/students", methods=["POST"])
@api_login_required
def add_student():
    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_student_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    try:
        student_id = create_student(cleaned_data)
    except sqlite3.IntegrityError as exc:
        return make_response(
            False,
            "Unable to create student.",
            status=409,
            errors=parse_student_integrity_error(str(exc)),
        )

    student = get_student(student_id)
    return make_response(True, "Student created.", data=dict(student), status=201)


@api_bp.route("/students/<int:student_id>", methods=["PUT"])
@api_login_required
def edit_student(student_id):
    if get_student(student_id) is None:
        return make_response(False, "Student not found.", status=404)

    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_student_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    try:
        update_student(student_id, cleaned_data)
    except sqlite3.IntegrityError as exc:
        return make_response(
            False,
            "Unable to update student.",
            status=409,
            errors=parse_student_integrity_error(str(exc)),
        )

    return make_response(True, "Student updated.", data=dict(get_student(student_id)))


@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
@api_login_required
def remove_student(student_id):
    student = get_student(student_id)
    if student is None:
        return make_response(False, "Student not found.", status=404)
    delete_student(student_id)
    return make_response(True, "Student deleted.")


@api_bp.route("/courses", methods=["GET"])
@api_login_required
def get_courses():
    courses = [dict(row) for row in list_courses()]
    return make_response(True, "Courses loaded.", data=courses)


@api_bp.route("/courses/<int:course_id>", methods=["GET"])
@api_login_required
def get_course_detail(course_id):
    course = get_course(course_id)
    if course is None:
        return make_response(False, "Course not found.", status=404)
    return make_response(True, "Course loaded.", data=dict(course))


@api_bp.route("/courses", methods=["POST"])
@api_login_required
def add_course():
    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_course_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    try:
        course_id = create_course(cleaned_data)
    except sqlite3.IntegrityError as exc:
        return make_response(
            False,
            "Unable to create course.",
            status=409,
            errors=parse_course_integrity_error(str(exc)),
        )

    return make_response(True, "Course created.", data=dict(get_course(course_id)), status=201)


@api_bp.route("/courses/<int:course_id>", methods=["PUT"])
@api_login_required
def edit_course(course_id):
    if get_course(course_id) is None:
        return make_response(False, "Course not found.", status=404)

    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_course_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    try:
        update_course(course_id, cleaned_data)
    except sqlite3.IntegrityError as exc:
        return make_response(
            False,
            "Unable to update course.",
            status=409,
            errors=parse_course_integrity_error(str(exc)),
        )

    return make_response(True, "Course updated.", data=dict(get_course(course_id)))


@api_bp.route("/courses/<int:course_id>", methods=["DELETE"])
@api_login_required
def remove_course(course_id):
    course = get_course(course_id)
    if course is None:
        return make_response(False, "Course not found.", status=404)
    delete_course(course_id)
    return make_response(True, "Course deleted.")


@api_bp.route("/registrations", methods=["GET"])
@api_login_required
def get_registration_list():
    student_id = request.args.get("student_id", type=int)
    registrations = [dict(row) for row in list_registrations(student_id=student_id)]
    return make_response(True, "Registrations loaded.", data=registrations)


@api_bp.route("/registrations/<int:registration_id>", methods=["GET"])
@api_login_required
def get_registration_detail(registration_id):
    registration = get_registration(registration_id)
    if registration is None:
        return make_response(False, "Registration not found.", status=404)
    return make_response(True, "Registration loaded.", data=dict(registration))


@api_bp.route("/registrations", methods=["POST"])
@api_login_required
def add_registration():
    payload = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_registration_payload(payload)
    if errors:
        return make_response(False, "Validation failed.", status=400, errors=errors)

    try:
        result = create_registrations(cleaned_data["student_id"], cleaned_data["course_ids"])
    except ValueError as exc:
        return make_response(False, str(exc), status=400)

    created_rows = [dict(row) for row in result["created"]]
    duplicate_rows = [dict(row) for row in result["duplicates"]]

    if not created_rows:
        return make_response(
            False,
            "Duplicate registrations prevented.",
            status=409,
            errors={"course_ids": "All selected courses are already registered for this student."},
            data={"duplicates": duplicate_rows},
        )

    status_code = 201
    message = "Registrations created."
    if duplicate_rows:
        message = "Registrations created with duplicates skipped."

    return make_response(
        True,
        message,
        status=status_code,
        data={"created": created_rows, "duplicates": duplicate_rows},
    )


@api_bp.route("/registrations/<int:registration_id>", methods=["DELETE"])
@api_login_required
def remove_registration(registration_id):
    deleted = delete_registration(registration_id)
    if not deleted:
        return make_response(False, "Registration not found.", status=404)
    return make_response(True, "Registration deleted.")


@api_bp.route("/lookup", methods=["GET"])
@api_login_required
def lookup_data():
    data = {
        "students": [dict(row) for row in list_student_choices()],
        "courses": [dict(row) for row in list_course_choices()],
    }
    return make_response(True, "Lookup data loaded.", data=data)
