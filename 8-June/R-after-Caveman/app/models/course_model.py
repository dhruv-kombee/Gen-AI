from app.db import execute_write, fetch_all, fetch_one


def list_courses():
    return fetch_all(
        """
        SELECT
            c.id,
            c.course_code,
            c.course_name,
            c.department,
            c.credit_hours,
            c.semester,
            c.created_at,
            c.updated_at,
            COUNT(r.id) AS registration_count
        FROM courses c
        LEFT JOIN registrations r ON r.course_id = c.id
        GROUP BY c.id
        ORDER BY c.course_code ASC
        """
    )


def list_course_choices():
    return fetch_all(
        """
        SELECT id, course_code, course_name, department, credit_hours, semester
        FROM courses
        ORDER BY course_code ASC
        """
    )


def get_course(course_id):
    return fetch_one(
        """
        SELECT *
        FROM courses
        WHERE id = ?
        """,
        (course_id,),
    )


def create_course(course_data):
    result = execute_write(
        """
        INSERT INTO courses (course_code, course_name, department, credit_hours, semester)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            course_data["course_code"],
            course_data["course_name"],
            course_data["department"],
            course_data["credit_hours"],
            course_data["semester"],
        ),
    )
    return result["lastrowid"]


def update_course(course_id, course_data):
    execute_write(
        """
        UPDATE courses
        SET
            course_code = ?,
            course_name = ?,
            department = ?,
            credit_hours = ?,
            semester = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            course_data["course_code"],
            course_data["course_name"],
            course_data["department"],
            course_data["credit_hours"],
            course_data["semester"],
            course_id,
        ),
    )


def delete_course(course_id):
    return execute_write("DELETE FROM courses WHERE id = ?", (course_id,))["rowcount"]

