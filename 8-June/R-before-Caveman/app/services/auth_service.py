import hmac

from flask import current_app


def validate_admin_credentials(username, password):
    expected_username = current_app.config["ADMIN_USERNAME"]
    expected_password = current_app.config["ADMIN_PASSWORD"]

    return hmac.compare_digest(username, expected_username) and hmac.compare_digest(password, expected_password)
