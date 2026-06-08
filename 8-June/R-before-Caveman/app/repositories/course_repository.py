from app.db import get_db


def list_courses():
    db = get_db()
    return db.execute(
        """
        SELECT
            c.*,
            COUNT(r.id) AS enrolled_students
        FROM courses c
        LEFT JOIN registrations r ON r.course_id = c.id
        GROUP BY c.id
        ORDER BY c.course_code COLLATE NOCASE ASC
        """
    ).fetchall()


def get_course(course_id):
    db = get_db()
    return db.execute(
        """
        SELECT
            c.*,
            COUNT(r.id) AS enrolled_students
        FROM courses c
        LEFT JOIN registrations r ON r.course_id = c.id
        WHERE c.id = ?
        GROUP BY c.id
        """,
        (course_id,),
    ).fetchone()


def create_course(data):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO courses (course_code, title, department, credits, capacity)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["course_code"],
            data["title"],
            data["department"],
            data["credits"],
            data["capacity"],
        ),
    )
    db.commit()
    return cursor.lastrowid


def update_course(course_id, data):
    db = get_db()
    cursor = db.execute(
        """
        UPDATE courses
        SET
            course_code = ?,
            title = ?,
            department = ?,
            credits = ?,
            capacity = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            data["course_code"],
            data["title"],
            data["department"],
            data["credits"],
            data["capacity"],
            course_id,
        ),
    )
    db.commit()
    return cursor.rowcount


def delete_course(course_id):
    db = get_db()
    cursor = db.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    db.commit()
    return cursor.rowcount


def course_code_exists(course_code, exclude_course_id=None):
    db = get_db()
    query = "SELECT id FROM courses WHERE course_code = ?"
    params = [course_code]
    if exclude_course_id:
        query += " AND id != ?"
        params.append(exclude_course_id)
    return db.execute(query, params).fetchone() is not None


def fetch_existing_course_ids(course_ids):
    if not course_ids:
        return set()

    placeholders = ",".join("?" for _ in course_ids)
    db = get_db()
    rows = db.execute(
        f"SELECT id FROM courses WHERE id IN ({placeholders})",
        course_ids,
    ).fetchall()
    return {row["id"] for row in rows}


def count_courses():
    db = get_db()
    return db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
