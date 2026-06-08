import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ENROLLMENT_PATTERN = re.compile(r"^[A-Za-z0-9/_-]{4,20}$")
PHONE_PATTERN = re.compile(r"^[0-9+\-\s]{7,15}$")


def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def validate_student_form(data):
    cleaned_data = {
        "full_name": clean_text(data.get("full_name")),
        "enrollment_number": clean_text(data.get("enrollment_number")).upper(),
        "email": clean_text(data.get("email")).lower(),
        "phone": clean_text(data.get("phone")),
        "department": clean_text(data.get("department")),
        "year": clean_text(data.get("year")),
    }
    errors = {}

    if len(cleaned_data["full_name"]) < 3:
        errors["full_name"] = "Student name must be at least 3 characters long."

    if not ENROLLMENT_PATTERN.match(cleaned_data["enrollment_number"]):
        errors["enrollment_number"] = "Use 4 to 20 letters, numbers, dashes, slashes, or underscores."

    if not EMAIL_PATTERN.match(cleaned_data["email"]):
        errors["email"] = "Enter a valid email address."

    if cleaned_data["phone"] and not PHONE_PATTERN.match(cleaned_data["phone"]):
        errors["phone"] = "Enter a valid phone number."

    if not cleaned_data["department"]:
        errors["department"] = "Please select a department."

    try:
        cleaned_data["year"] = int(cleaned_data["year"])
        if cleaned_data["year"] < 1 or cleaned_data["year"] > 6:
            errors["year"] = "Academic year must be between 1 and 6."
    except (TypeError, ValueError):
        errors["year"] = "Please choose a valid academic year."

    return cleaned_data, errors


def validate_course_form(data):
    cleaned_data = {
        "course_code": clean_text(data.get("course_code")).upper(),
        "title": clean_text(data.get("title")),
        "department": clean_text(data.get("department")),
        "credits": clean_text(data.get("credits")),
        "capacity": clean_text(data.get("capacity")),
    }
    errors = {}

    if len(cleaned_data["course_code"]) < 4 or len(cleaned_data["course_code"]) > 12:
        errors["course_code"] = "Course code must be between 4 and 12 characters."

    if len(cleaned_data["title"]) < 5:
        errors["title"] = "Course title must be at least 5 characters long."

    if not cleaned_data["department"]:
        errors["department"] = "Please select a department."

    try:
        cleaned_data["credits"] = int(cleaned_data["credits"])
        if cleaned_data["credits"] < 1 or cleaned_data["credits"] > 6:
            errors["credits"] = "Credits must be between 1 and 6."
    except (TypeError, ValueError):
        errors["credits"] = "Please provide a valid credit value."

    try:
        cleaned_data["capacity"] = int(cleaned_data["capacity"])
        if cleaned_data["capacity"] < 1 or cleaned_data["capacity"] > 500:
            errors["capacity"] = "Capacity must be between 1 and 500."
    except (TypeError, ValueError):
        errors["capacity"] = "Please provide a valid capacity."

    return cleaned_data, errors


def validate_registration_form(data, require_courses=True):
    cleaned_data = {
        "student_id": clean_text(data.get("student_id")),
        "course_ids": data.get("course_ids") or [],
    }
    errors = {}

    try:
        cleaned_data["student_id"] = int(cleaned_data["student_id"])
        if cleaned_data["student_id"] < 1:
            errors["student_id"] = "Please choose a valid student."
    except (TypeError, ValueError):
        errors["student_id"] = "Please choose a student."

    if isinstance(cleaned_data["course_ids"], str):
        cleaned_data["course_ids"] = [cleaned_data["course_ids"]]

    parsed_course_ids = []
    for course_id in cleaned_data["course_ids"]:
        try:
            parsed_value = int(course_id)
            if parsed_value > 0 and parsed_value not in parsed_course_ids:
                parsed_course_ids.append(parsed_value)
        except (TypeError, ValueError):
            continue

    cleaned_data["course_ids"] = parsed_course_ids

    if require_courses and not cleaned_data["course_ids"]:
        errors["course_ids"] = "Select at least one course."

    return cleaned_data, errors
