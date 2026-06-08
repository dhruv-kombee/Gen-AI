from app.db import get_db


def list_registrations():
    db = get_db()
    return db.execute(
        """
        SELECT
            r.id,
            r.registered_at,
            s.id AS student_id,
            s.full_name,
            s.enrollment_number,
            c.id AS course_id,
            c.course_code,
            c.title AS course_title
        FROM registrations r
        INNER JOIN students s ON s.id = r.student_id
        INNER JOIN courses c ON c.id = r.course_id
        ORDER BY r.registered_at DESC, s.full_name COLLATE NOCASE ASC
        """
    ).fetchall()


def get_registration(registration_id):
    db = get_db()
    return db.execute(
        """
        SELECT
            r.id,
            r.registered_at,
            s.id AS student_id,
            s.full_name,
            s.enrollment_number,
            c.id AS course_id,
            c.course_code,
            c.title AS course_title
        FROM registrations r
        INNER JOIN students s ON s.id = r.student_id
        INNER JOIN courses c ON c.id = r.course_id
        WHERE r.id = ?
        """,
        (registration_id,),
    ).fetchone()


def get_recent_registrations(limit=5):
    db = get_db()
    return db.execute(
        """
        SELECT
            r.id,
            r.registered_at,
            s.full_name,
            s.enrollment_number,
            c.course_code,
            c.title AS course_title
        FROM registrations r
        INNER JOIN students s ON s.id = r.student_id
        INNER JOIN courses c ON c.id = r.course_id
        ORDER BY r.registered_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def get_courses_for_student(student_id):
    db = get_db()
    return db.execute(
        """
        SELECT
            r.id AS registration_id,
            c.id AS course_id,
            c.course_code,
            c.title,
            c.credits,
            r.registered_at
        FROM registrations r
        INNER JOIN courses c ON c.id = r.course_id
        WHERE r.student_id = ?
        ORDER BY c.course_code COLLATE NOCASE ASC
        """,
        (student_id,),
    ).fetchall()


def get_student_registration_overview():
    db = get_db()
    return db.execute(
        """
        SELECT
            s.id AS student_id,
            s.full_name,
            s.enrollment_number,
            s.department,
            s.year,
            r.id AS registration_id,
            c.id AS course_id,
            c.course_code,
            c.title
        FROM students s
        LEFT JOIN registrations r ON r.student_id = s.id
        LEFT JOIN courses c ON c.id = r.course_id
        ORDER BY s.full_name COLLATE NOCASE ASC, c.course_code COLLATE NOCASE ASC
        """
    ).fetchall()


def create_registrations(student_id, course_ids):
    db = get_db()
    unique_course_ids = list(dict.fromkeys(course_ids))
    if not unique_course_ids:
        return {"created_count": 0, "duplicate_course_ids": [], "created_course_ids": []}

    placeholders = ",".join("?" for _ in unique_course_ids)
    existing_rows = db.execute(
        f"""
        SELECT course_id
        FROM registrations
        WHERE student_id = ? AND course_id IN ({placeholders})
        """,
        [student_id, *unique_course_ids],
    ).fetchall()
    existing_course_ids = {row["course_id"] for row in existing_rows}
    new_course_ids = [course_id for course_id in unique_course_ids if course_id not in existing_course_ids]

    if new_course_ids:
        db.executemany(
            "INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
            [(student_id, course_id) for course_id in new_course_ids],
        )
        db.commit()

    return {
        "created_count": len(new_course_ids),
        "duplicate_course_ids": sorted(existing_course_ids),
        "created_course_ids": new_course_ids,
    }


def replace_student_registrations(student_id, course_ids):
    db = get_db()
    normalized_course_ids = list(dict.fromkeys(course_ids))

    current_rows = db.execute(
        "SELECT course_id FROM registrations WHERE student_id = ?",
        (student_id,),
    ).fetchall()
    current_course_ids = {row["course_id"] for row in current_rows}
    target_course_ids = set(normalized_course_ids)

    course_ids_to_add = sorted(target_course_ids - current_course_ids)
    course_ids_to_remove = sorted(current_course_ids - target_course_ids)

    if course_ids_to_remove:
        placeholders = ",".join("?" for _ in course_ids_to_remove)
        db.execute(
            f"""
            DELETE FROM registrations
            WHERE student_id = ? AND course_id IN ({placeholders})
            """,
            [student_id, *course_ids_to_remove],
        )

    if course_ids_to_add:
        db.executemany(
            "INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
            [(student_id, course_id) for course_id in course_ids_to_add],
        )

    db.commit()
    return {
        "added_course_ids": course_ids_to_add,
        "removed_course_ids": course_ids_to_remove,
    }


def delete_registration(registration_id):
    db = get_db()
    cursor = db.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
    db.commit()
    return cursor.rowcount


def count_registrations():
    db = get_db()
    return db.execute("SELECT COUNT(*) FROM registrations").fetchone()[0]
