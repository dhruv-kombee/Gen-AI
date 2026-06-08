from app.db import get_db


def list_students(search_term=None):
    db = get_db()
    query = """
        SELECT
            s.*,
            COUNT(r.id) AS registration_count
        FROM students s
        LEFT JOIN registrations r ON r.student_id = s.id
    """
    params = []

    if search_term:
        query += " WHERE s.full_name LIKE ? OR s.enrollment_number LIKE ?"
        like_term = f"%{search_term.strip()}%"
        params.extend([like_term, like_term])

    query += """
        GROUP BY s.id
        ORDER BY s.full_name COLLATE NOCASE ASC
    """
    return db.execute(query, params).fetchall()


def get_student(student_id):
    db = get_db()
    return db.execute(
        """
        SELECT
            s.*,
            COUNT(r.id) AS registration_count
        FROM students s
        LEFT JOIN registrations r ON r.student_id = s.id
        WHERE s.id = ?
        GROUP BY s.id
        """,
        (student_id,),
    ).fetchone()


def create_student(data):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO students (full_name, enrollment_number, email, phone, department, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["full_name"],
            data["enrollment_number"],
            data["email"],
            data["phone"],
            data["department"],
            data["year"],
        ),
    )
    db.commit()
    return cursor.lastrowid


def update_student(student_id, data):
    db = get_db()
    cursor = db.execute(
        """
        UPDATE students
        SET
            full_name = ?,
            enrollment_number = ?,
            email = ?,
            phone = ?,
            department = ?,
            year = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            data["full_name"],
            data["enrollment_number"],
            data["email"],
            data["phone"],
            data["department"],
            data["year"],
            student_id,
        ),
    )
    db.commit()
    return cursor.rowcount


def delete_student(student_id):
    db = get_db()
    cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    return cursor.rowcount


def enrollment_exists(enrollment_number, exclude_student_id=None):
    db = get_db()
    query = "SELECT id FROM students WHERE enrollment_number = ?"
    params = [enrollment_number]
    if exclude_student_id:
        query += " AND id != ?"
        params.append(exclude_student_id)
    return db.execute(query, params).fetchone() is not None


def email_exists(email, exclude_student_id=None):
    db = get_db()
    query = "SELECT id FROM students WHERE email = ?"
    params = [email]
    if exclude_student_id:
        query += " AND id != ?"
        params.append(exclude_student_id)
    return db.execute(query, params).fetchone() is not None


def count_students():
    db = get_db()
    return db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
