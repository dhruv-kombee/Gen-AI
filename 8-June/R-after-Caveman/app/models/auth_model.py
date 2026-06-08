from app.db import fetch_one


def get_admin_by_username(username):
    return fetch_one("SELECT * FROM admins WHERE username = ?", (username,))

