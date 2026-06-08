from datetime import datetime

from flask import Flask

from app.config import Config
from app.controllers.api_controller import api_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.course_controller import course_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.error_controller import register_error_handlers
from app.controllers.registration_controller import registration_bp
from app.controllers.student_controller import student_bp
from app.db import close_db, initialize_database


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.teardown_appcontext(close_db)

    with app.app_context():
        initialize_database()

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(api_bp)

    register_error_handlers(app)

    @app.context_processor
    def inject_template_helpers():
        return {"current_year": datetime.now().year}

    return app

