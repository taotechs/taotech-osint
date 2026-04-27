"""Username OSINT API routes."""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.services.osint_bridge import (
    OsintExecutionTimeout,
    OsintBridgeError,
    run_username_scan,
)
from backend.utils.response import error_response, success_response
from backend.utils.validators import is_valid_username

username_bp = Blueprint("username_routes", __name__)


@username_bp.get("/api/osint/username")
def username_scan():
    """GET /api/osint/username?username=xxx."""
    username = (request.args.get("username") or "").strip()
    if not is_valid_username(username):
        current_app.logger.warning("Username scan validation failed: %s", username)
        return error_response(
            "Invalid username. Use 3-30 chars: letters, numbers, _, ., -",
            400,
            error_code="VALIDATION_ERROR",
        )

    try:
        payload = run_username_scan(username)
        current_app.logger.info("Username scan completed successfully: %s", username)
        return success_response(payload, "Username scan completed.")
    except OsintExecutionTimeout as exc:
        current_app.logger.error("Username scan timeout for %s: %s", username, exc)
        return error_response(
            "Username scan timed out.",
            504,
            details=str(exc),
            error_code="SCAN_TIMEOUT",
        )
    except OsintBridgeError as exc:
        current_app.logger.error("Username scan service failure for %s: %s", username, exc)
        return error_response(
            "Username scan failed.",
            500,
            details=str(exc),
            error_code="SCAN_FAILED",
        )
