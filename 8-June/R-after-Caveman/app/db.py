import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE_PATH"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def fetch_all(query, params=()):
    cursor = get_db().execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def fetch_one(query, params=()):
    cursor = get_db().execute(query, params)
    row = cursor.fetchone()
    cursor.close()
    return row


def execute_write(query, params=()):
    db = get_db()
    cursor = db.execute(query, params)
    db.commit()
    result = {"lastrowid": cursor.lastrowid, "rowcount": cursor.rowcount}
    cursor.close()
    return result


def execute_many(query, params):
    db = get_db()
    cursor = db.executemany(query, params)
    db.commit()
    result = {"rowcount": cursor.rowcount}
    cursor.close()
    return result


def initialize_database():
    database_path = Path(current_app.config["DATABASE_PATH"])
    database_path.parent.mkdir(parents=True, exist_ok=True)

    should_seed = not database_path.exists()
    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        schema_path = current_app.config["BASE_DIR"] / "schema.sql"
        sample_data_path = current_app.config["BASE_DIR"] / "sample_data.sql"

        if should_seed:
            connection.executescript(schema_path.read_text(encoding="utf-8"))
            connection.executescript(sample_data_path.read_text(encoding="utf-8"))
            connection.commit()
            return

        existing_tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'students'"
        ).fetchone()

        if existing_tables is None:
            connection.executescript(schema_path.read_text(encoding="utf-8"))
            connection.executescript(sample_data_path.read_text(encoding="utf-8"))
            connection.commit()
    finally:
        connection.close()

