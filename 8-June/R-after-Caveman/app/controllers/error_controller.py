from flask import jsonify, render_template, request


def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(_error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Resource not found."}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.exception("Unhandled application error: %s", error)
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Internal server error."}), 500
        return render_template("errors/500.html"), 500

