from flask import Blueprint, abort, jsonify, request

from app.repositories import course_repository
from app.repositories import registration_repository
from app.repositories import student_repository
from app.utils.decorators import login_required
from app.utils.validators import validate_course_form
from app.utils.validators import validate_registration_form
from app.utils.validators import validate_student_form


api_bp = Blueprint("api", __name__, url_prefix="/api")


def _row_to_dict(row):
    return dict(row) if row is not None else None


def _rows_to_dicts(rows):
    return [dict(row) for row in rows]


@api_bp.get("/students")
@login_required
def api_list_students():
    search_term = (request.args.get("search") or "").strip()
    students = student_repository.list_students(search_term=search_term)
    return jsonify({"success": True, "data": _rows_to_dicts(students)})


@api_bp.get("/students/<int:student_id>")
@login_required
def api_get_student(student_id):
    student = student_repository.get_student(student_id)
    if student is None:
        abort(404)
    return jsonify({"success": True, "data": _row_to_dict(student)})


@api_bp.post("/students")
@login_required
def api_create_student():
    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_student_form(payload)

    if student_repository.enrollment_exists(cleaned_data["enrollment_number"]):
        errors["enrollment_number"] = "This enrollment number is already in use."

    if student_repository.email_exists(cleaned_data["email"]):
        errors["email"] = "This email address is already in use."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    student_id = student_repository.create_student(cleaned_data)
    student = student_repository.get_student(student_id)
    return jsonify({"success": True, "data": _row_to_dict(student)}), 201


@api_bp.put("/students/<int:student_id>")
@login_required
def api_update_student(student_id):
    student = student_repository.get_student(student_id)
    if student is None:
        abort(404)

    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_student_form(payload)

    if student_repository.enrollment_exists(cleaned_data["enrollment_number"], exclude_student_id=student_id):
        errors["enrollment_number"] = "This enrollment number is already in use."

    if student_repository.email_exists(cleaned_data["email"], exclude_student_id=student_id):
        errors["email"] = "This email address is already in use."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    student_repository.update_student(student_id, cleaned_data)
    updated_student = student_repository.get_student(student_id)
    return jsonify({"success": True, "data": _row_to_dict(updated_student)})


@api_bp.delete("/students/<int:student_id>")
@login_required
def api_delete_student(student_id):
    if student_repository.get_student(student_id) is None:
        abort(404)

    student_repository.delete_student(student_id)
    return jsonify({"success": True, "message": "Student deleted successfully."})


@api_bp.get("/courses")
@login_required
def api_list_courses():
    courses = course_repository.list_courses()
    return jsonify({"success": True, "data": _rows_to_dicts(courses)})


@api_bp.get("/courses/<int:course_id>")
@login_required
def api_get_course(course_id):
    course = course_repository.get_course(course_id)
    if course is None:
        abort(404)
    return jsonify({"success": True, "data": _row_to_dict(course)})


@api_bp.post("/courses")
@login_required
def api_create_course():
    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_course_form(payload)

    if course_repository.course_code_exists(cleaned_data["course_code"]):
        errors["course_code"] = "This course code is already in use."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    course_id = course_repository.create_course(cleaned_data)
    course = course_repository.get_course(course_id)
    return jsonify({"success": True, "data": _row_to_dict(course)}), 201


@api_bp.put("/courses/<int:course_id>")
@login_required
def api_update_course(course_id):
    course = course_repository.get_course(course_id)
    if course is None:
        abort(404)

    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_course_form(payload)

    if course_repository.course_code_exists(cleaned_data["course_code"], exclude_course_id=course_id):
        errors["course_code"] = "This course code is already in use."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    course_repository.update_course(course_id, cleaned_data)
    updated_course = course_repository.get_course(course_id)
    return jsonify({"success": True, "data": _row_to_dict(updated_course)})


@api_bp.delete("/courses/<int:course_id>")
@login_required
def api_delete_course(course_id):
    if course_repository.get_course(course_id) is None:
        abort(404)

    course_repository.delete_course(course_id)
    return jsonify({"success": True, "message": "Course deleted successfully."})


@api_bp.get("/registrations")
@login_required
def api_list_registrations():
    registrations = registration_repository.list_registrations()
    return jsonify({"success": True, "data": _rows_to_dicts(registrations)})


@api_bp.get("/registrations/<int:registration_id>")
@login_required
def api_get_registration(registration_id):
    registration = registration_repository.get_registration(registration_id)
    if registration is None:
        abort(404)
    return jsonify({"success": True, "data": _row_to_dict(registration)})


@api_bp.post("/registrations")
@login_required
def api_create_registrations():
    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_registration_form(payload)

    student = student_repository.get_student(cleaned_data["student_id"]) if not errors.get("student_id") else None
    if student is None and not errors.get("student_id"):
        errors["student_id"] = "Selected student does not exist."

    existing_course_ids = course_repository.fetch_existing_course_ids(cleaned_data["course_ids"])
    missing_course_ids = sorted(set(cleaned_data["course_ids"]) - existing_course_ids)
    if missing_course_ids:
        errors["course_ids"] = "One or more selected courses do not exist."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    result = registration_repository.create_registrations(cleaned_data["student_id"], cleaned_data["course_ids"])
    status_code = 201 if result["created_count"] > 0 else 409
    return (
        jsonify(
            {
                "success": result["created_count"] > 0,
                "message": "Registrations processed.",
                "data": result,
            }
        ),
        status_code,
    )


@api_bp.put("/students/<int:student_id>/registrations")
@login_required
def api_replace_student_registrations(student_id):
    student = student_repository.get_student(student_id)
    if student is None:
        abort(404)

    payload = request.get_json(silent=True) or {}
    cleaned_data, errors = validate_registration_form(
        {"student_id": student_id, "course_ids": payload.get("course_ids", [])},
        require_courses=False,
    )

    existing_course_ids = course_repository.fetch_existing_course_ids(cleaned_data["course_ids"])
    missing_course_ids = sorted(set(cleaned_data["course_ids"]) - existing_course_ids)
    if missing_course_ids:
        errors["course_ids"] = "One or more selected courses do not exist."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    result = registration_repository.replace_student_registrations(student_id, cleaned_data["course_ids"])
    courses = registration_repository.get_courses_for_student(student_id)
    return jsonify(
        {
            "success": True,
            "message": "Student registrations updated successfully.",
            "data": {
                "changes": result,
                "courses": _rows_to_dicts(courses),
            },
        }
    )


@api_bp.delete("/registrations/<int:registration_id>")
@login_required
def api_delete_registration(registration_id):
    if registration_repository.get_registration(registration_id) is None:
        abort(404)

    registration_repository.delete_registration(registration_id)
    return jsonify({"success": True, "message": "Registration deleted successfully."})
