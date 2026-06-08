import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ENROLLMENT_PATTERN = re.compile(r"^[A-Za-z0-9\-/]{4,20}$")
PHONE_PATTERN = re.compile(r"^[0-9+\-\s]{7,15}$")
COURSE_CODE_PATTERN = re.compile(r"^[A-Za-z0-9\-]{3,15}$")


def _clean_text(value):
    return value.strip() if isinstance(value, str) else value


def validate_login_payload(data):
    username = _clean_text(data.get("username", ""))
    password = _clean_text(data.get("password", ""))
    errors = {}

    if not username:
        errors["username"] = "Username is required."
    if not password:
        errors["password"] = "Password is required."

    return errors, {"username": username, "password": password}


def validate_student_payload(data):
    full_name = _clean_text(data.get("full_name", ""))
    enrollment_number = _clean_text(data.get("enrollment_number", ""))
    email = _clean_text(data.get("email", ""))
    phone = _clean_text(data.get("phone", ""))
    department = _clean_text(data.get("department", ""))
    raw_year_level = data.get("year_level", "")
    errors = {}

    if not full_name or len(full_name) < 3:
        errors["full_name"] = "Full name must be at least 3 characters."
    if not enrollment_number or not ENROLLMENT_PATTERN.match(enrollment_number):
        errors["enrollment_number"] = "Use 4 to 20 letters, numbers, hyphens, or slashes."
    if not email or not EMAIL_PATTERN.match(email):
        errors["email"] = "Enter a valid email address."
    if phone and not PHONE_PATTERN.match(phone):
        errors["phone"] = "Use 7 to 15 digits, spaces, plus, or hyphen."
    if not department:
        errors["department"] = "Department is required."

    try:
        year_level = int(raw_year_level)
        if year_level < 1 or year_level > 8:
            raise ValueError
    except (TypeError, ValueError):
        errors["year_level"] = "Year level must be between 1 and 8."
        year_level = raw_year_level

    cleaned = {
        "full_name": full_name,
        "enrollment_number": enrollment_number.upper(),
        "email": email.lower(),
        "phone": phone,
        "department": department,
        "year_level": year_level,
    }
    return errors, cleaned


def validate_course_payload(data):
    course_code = _clean_text(data.get("course_code", ""))
    course_name = _clean_text(data.get("course_name", ""))
    department = _clean_text(data.get("department", ""))
    semester = _clean_text(data.get("semester", ""))
    raw_credit_hours = data.get("credit_hours", "")
    errors = {}

    if not course_code or not COURSE_CODE_PATTERN.match(course_code):
        errors["course_code"] = "Course code should be 3 to 15 characters."
    if not course_name or len(course_name) < 4:
        errors["course_name"] = "Course name must be at least 4 characters."
    if not department:
        errors["department"] = "Department is required."
    if not semester:
        errors["semester"] = "Semester is required."

    try:
        credit_hours = int(raw_credit_hours)
        if credit_hours < 1 or credit_hours > 6:
            raise ValueError
    except (TypeError, ValueError):
        errors["credit_hours"] = "Credit hours must be between 1 and 6."
        credit_hours = raw_credit_hours

    cleaned = {
        "course_code": course_code.upper(),
        "course_name": course_name,
        "department": department,
        "credit_hours": credit_hours,
        "semester": semester,
    }
    return errors, cleaned


def validate_registration_payload(data):
    raw_student_id = data.get("student_id")
    raw_course_ids = data.get("course_ids", [])
    errors = {}

    if isinstance(raw_course_ids, str):
        raw_course_ids = [raw_course_ids]

    try:
        student_id = int(raw_student_id)
    except (TypeError, ValueError):
        errors["student_id"] = "Select a valid student."
        student_id = raw_student_id

    cleaned_course_ids = []
    for course_id in raw_course_ids:
        try:
            cleaned_course_ids.append(int(course_id))
        except (TypeError, ValueError):
            errors["course_ids"] = "Select valid courses."
            break

    cleaned_course_ids = list(dict.fromkeys(cleaned_course_ids))

    if not cleaned_course_ids and "course_ids" not in errors:
        errors["course_ids"] = "Select at least one course."

    return errors, {"student_id": student_id, "course_ids": cleaned_course_ids}


def parse_student_integrity_error(error_text):
    normalized = error_text.lower()
    if "students.enrollment_number" in normalized or "enrollment_number" in normalized:
        return {"enrollment_number": "Enrollment number already exists."}
    if "students.email" in normalized or "email" in normalized:
        return {"email": "Email address already exists."}
    return {"general": "Unable to save the student record."}


def parse_course_integrity_error(error_text):
    normalized = error_text.lower()
    if "courses.course_code" in normalized or "course_code" in normalized:
        return {"course_code": "Course code already exists."}
    return {"general": "Unable to save the course record."}
