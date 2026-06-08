from app.db import fetch_all, fetch_one


def get_dashboard_metrics():
    total_students = fetch_one("SELECT COUNT(*) AS total FROM students")["total"]
    total_courses = fetch_one("SELECT COUNT(*) AS total FROM courses")["total"]
    total_registrations = fetch_one("SELECT COUNT(*) AS total FROM registrations")["total"]
    recent_registrations = fetch_all(
        """
        SELECT
            r.id,
            r.created_at,
            s.full_name,
            s.enrollment_number,
            c.course_code,
            c.course_name
        FROM registrations r
        INNER JOIN students s ON s.id = r.student_id
        INNER JOIN courses c ON c.id = r.course_id
        ORDER BY r.created_at DESC
        LIMIT 6
        """
    )

    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_registrations": total_registrations,
        "recent_registrations": recent_registrations,
    }

