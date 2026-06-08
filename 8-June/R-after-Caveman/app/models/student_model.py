from app.db import execute_write, fetch_all, fetch_one


STUDENT_SELECT = """
    SELECT
        s.id,
        s.full_name,
        s.enrollment_number,
        s.email,
        s.phone,
        s.department,
        s.year_level,
        s.created_at,
        s.updated_at,
        COALESCE(reg_summary.registered_courses, '') AS registered_courses,
        COALESCE(reg_summary.registration_count, 0) AS registration_count
    FROM students s
    LEFT JOIN (
        SELECT
            r.student_id,
            GROUP_CONCAT(c.course_code || ' - ' || c.course_name, ', ') AS registered_courses,
            COUNT(r.id) AS registration_count
        FROM registrations r
        INNER JOIN courses c ON c.id = r.course_id
        GROUP BY r.student_id
    ) reg_summary ON reg_summary.student_id = s.id
"""


def list_students(search=""):
    params = []
    query = STUDENT_SELECT

    if search:
        query += """
            WHERE s.full_name LIKE ? OR s.enrollment_number LIKE ?
        """
        search_term = f"%{search}%"
        params.extend([search_term, search_term])

    query += " ORDER BY s.created_at DESC, s.full_name ASC"
    return fetch_all(query, tuple(params))


def list_student_choices():
    return fetch_all(
        """
        SELECT id, full_name, enrollment_number
        FROM students
        ORDER BY full_name ASC
        """
    )


def get_student(student_id):
    return fetch_one(f"{STUDENT_SELECT} WHERE s.id = ?", (student_id,))


def create_student(student_data):
    result = execute_write(
        """
        INSERT INTO students (full_name, enrollment_number, email, phone, department, year_level)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            student_data["full_name"],
            student_data["enrollment_number"],
            student_data["email"],
            student_data["phone"],
            student_data["department"],
            student_data["year_level"],
        ),
    )
    return result["lastrowid"]


def update_student(student_id, student_data):
    execute_write(
        """
        UPDATE students
        SET
            full_name = ?,
            enrollment_number = ?,
            email = ?,
            phone = ?,
            department = ?,
            year_level = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            student_data["full_name"],
            student_data["enrollment_number"],
            student_data["email"],
            student_data["phone"],
            student_data["department"],
            student_data["year_level"],
            student_id,
        ),
    )


def delete_student(student_id):
    return execute_write("DELETE FROM students WHERE id = ?", (student_id,))["rowcount"]

