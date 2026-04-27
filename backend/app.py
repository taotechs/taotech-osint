"""Flask API entry point for Taotech OSINT Toolkit backend."""

from __future__ import annotations

from flask import Flask, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from backend.routes.domain_routes import domain_bp
from backend.routes.email_routes import email_bp
from backend.routes.username_routes import username_bp
from core.reporting.report_generator import CORE_REPORTS_DIR
from backend.services.osint_bridge import list_html_reports
from backend.utils.logger import get_backend_logger
from backend.utils.response import error_response, success_response


def create_app() -> Flask:
    """Application factory for easy testing and future scaling."""
    app = Flask(__name__)
    CORS(app)  # Enables cross-origin requests for React frontend integration.

    logger = get_backend_logger("logs.txt")
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.propagate = False

    @app.before_request
    def log_request_start() -> None:
        """Log every incoming request method and path."""
        logger.info(
            "Incoming request: %s %s | ip=%s",
            request.method,
            request.path,
            request.remote_addr,
        )

    @app.after_request
    def log_request_end(response):
        """Log request completion with HTTP status code."""
        logger.info(
            "Completed request: %s %s -> %s",
            request.method,
            request.path,
            response.status_code,
        )
        return response

    @app.get("/api/health")
    def health_check():
        """Simple health endpoint for uptime checks."""
        return success_response({"status": "ok"}, "API is healthy.")

    @app.get("/api/reports")
    def reports():
        """List generated HTML reports in /reports."""
        try:
            data = list_html_reports()
            logger.info("Reports fetched successfully.")
            return success_response(data, "Reports fetched.")
        except Exception as exc:
            logger.exception("Reports fetch failed: %s", exc)
            return error_response(
                "Failed to fetch reports.",
                500,
                details=str(exc),
                error_code="REPORTS_FETCH_FAILED",
            )

    @app.get("/api/reports/view/<path:filename>")
    def view_report(filename: str):
        """Open structured HTML report in browser."""
        reports_dir = CORE_REPORTS_DIR.resolve()
        return send_from_directory(reports_dir, filename)

    @app.get("/api/reports/download/<path:filename>")
    def download_report(filename: str):
        """Download report file as an attachment."""
        reports_dir = CORE_REPORTS_DIR.resolve()
        return send_from_directory(reports_dir, filename, as_attachment=True)

    @app.errorhandler(404)
    def handle_not_found(error):
        """Return a JSON 404 response for unknown API paths."""
        logger.warning("Not found: %s %s", request.method, request.path)
        if request.path.startswith("/api/"):
            return error_response(
                "Resource not found.",
                404,
                details=str(error),
                error_code="NOT_FOUND",
            )
        return error

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Return a JSON response for unhandled API exceptions."""
        if isinstance(error, HTTPException):
            logger.warning(
                "HTTP exception: %s %s -> %s",
                request.method,
                request.path,
                error.code,
            )
            if request.path.startswith("/api/"):
                return error_response(
                    error.description or "HTTP error.",
                    error.code or 500,
                    error_code="HTTP_EXCEPTION",
                )
            return error

        logger.exception("Unhandled Flask error at %s: %s", request.path, error)
        if request.path.startswith("/api/"):
            return error_response(
                "Internal server error.",
                500,
                details=str(error),
                error_code="INTERNAL_ERROR",
            )
        return error

    # Register modular route blueprints.
    app.register_blueprint(username_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(domain_bp)

    return app


app = create_app()


if __name__ == "__main__":
    # Debug can be disabled in production deployment.
    app.run(host="0.0.0.0", port=5000, debug=True)
