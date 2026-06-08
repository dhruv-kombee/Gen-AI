import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE_PATH"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def initialize_database(app):
    database_path = Path(app.config["DATABASE_PATH"])
    database_path.parent.mkdir(parents=True, exist_ok=True)

    schema_sql = Path(app.config["SCHEMA_PATH"]).read_text(encoding="utf-8")
    sample_data_sql = Path(app.config["SAMPLE_DATA_PATH"]).read_text(encoding="utf-8")

    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema_sql)

        student_count = connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        course_count = connection.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        if student_count == 0 and course_count == 0:
            connection.executescript(sample_data_sql)

        connection.commit()
