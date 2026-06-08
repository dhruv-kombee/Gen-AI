from app.db import execute_many, execute_write, fetch_all, fetch_one, get_db


REGISTRATION_SELECT = """
    SELECT
        r.id,
        r.student_id,
        r.course_id,
        r.created_at,
        s.full_name,
        s.enrollment_number,
        c.course_code,
        c.course_name,
        c.department,
        c.semester
    FROM registrations r
    INNER JOIN students s ON s.id = r.student_id
    INNER JOIN courses c ON c.id = r.course_id
"""


def list_registrations(student_id=None, limit=None):
    query = REGISTRATION_SELECT
    params = []

    if student_id is not None:
        query += " WHERE r.student_id = ?"
        params.append(student_id)

    query += " ORDER BY r.created_at DESC, s.full_name ASC"

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    return fetch_all(query, tuple(params))


def get_registration(registration_id):
    return fetch_one(f"{REGISTRATION_SELECT} WHERE r.id = ?", (registration_id,))


def create_registrations(student_id, course_ids):
    unique_course_ids = list(dict.fromkeys(course_ids))
    placeholder = ", ".join("?" for _ in unique_course_ids)

    student = fetch_one("SELECT id, full_name, enrollment_number FROM students WHERE id = ?", (student_id,))
    if student is None:
        raise ValueError("Student not found.")

    course_rows = fetch_all(
        f"""
        SELECT id, course_code, course_name
        FROM courses
        WHERE id IN ({placeholder})
        ORDER BY course_code ASC
        """,
        tuple(unique_course_ids),
    )

    available_course_ids = {row["id"] for row in course_rows}
    missing_course_ids = [course_id for course_id in unique_course_ids if course_id not in available_course_ids]
    if missing_course_ids:
        raise ValueError("One or more selected courses do not exist.")

    duplicate_rows = fetch_all(
        f"""
        SELECT c.id, c.course_code, c.course_name
        FROM registrations r
        INNER JOIN courses c ON c.id = r.course_id
        WHERE r.student_id = ? AND r.course_id IN ({placeholder})
        ORDER BY c.course_code ASC
        """,
        (student_id, *unique_course_ids),
    )
    duplicate_ids = {row["id"] for row in duplicate_rows}
    new_course_ids = [course_id for course_id in unique_course_ids if course_id not in duplicate_ids]

    if new_course_ids:
        execute_many(
            "INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
            [(student_id, course_id) for course_id in new_course_ids],
        )

    created_rows = []
    if new_course_ids:
        new_placeholder = ", ".join("?" for _ in new_course_ids)
        created_rows = fetch_all(
            f"""
            {REGISTRATION_SELECT}
            WHERE r.student_id = ? AND r.course_id IN ({new_placeholder})
            ORDER BY r.created_at DESC
            """,
            (student_id, *new_course_ids),
        )

    return {"student": student, "created": created_rows, "duplicates": duplicate_rows}


def delete_registration(registration_id):
    return execute_write("DELETE FROM registrations WHERE id = ?", (registration_id,))["rowcount"]

