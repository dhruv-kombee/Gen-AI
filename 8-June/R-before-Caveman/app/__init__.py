from flask import Flask, jsonify, render_template, request

from app.controllers.api_controller import api_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.course_controller import courses_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.registration_controller import registrations_bp
from app.controllers.student_controller import students_bp
from app.db import init_app as init_db_app
from app.db import initialize_database
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db_app(app)
    initialize_database(app)

    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(api_bp)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Bad request."}), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Resource not found."}), 404
        return render_template("errors/404.html", message="The page you requested does not exist."), 404

    @app.errorhandler(500)
    def server_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "An unexpected server error occurred."}), 500
        return render_template("errors/500.html"), 500
