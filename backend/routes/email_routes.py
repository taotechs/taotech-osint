"""Email OSINT API routes."""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.services.osint_bridge import (
    OsintExecutionTimeout,
    OsintBridgeError,
    run_email_scan,
)
from backend.utils.response import error_response, success_response
from backend.utils.validators import is_valid_email

email_bp = Blueprint("email_routes", __name__)


@email_bp.get("/api/osint/email")
def email_scan():
    """GET /api/osint/email?email=xxx."""
    email = (request.args.get("email") or "").strip()
    if not is_valid_email(email):
        current_app.logger.warning("Email scan validation failed: %s", email)
        return error_response(
            "Invalid email format.",
            400,
            error_code="VALIDATION_ERROR",
        )

    try:
        payload = run_email_scan(email)
        current_app.logger.info("Email scan completed successfully: %s", email)
        return success_response(payload, "Email scan completed.")
    except OsintExecutionTimeout as exc:
        current_app.logger.error("Email scan timeout for %s: %s", email, exc)
        return error_response(
            "Email scan timed out.",
            504,
            details=str(exc),
            error_code="SCAN_TIMEOUT",
        )
    except OsintBridgeError as exc:
        current_app.logger.error("Email scan service failure for %s: %s", email, exc)
        return error_response(
            "Email scan failed.",
            500,
            details=str(exc),
            error_code="SCAN_FAILED",
        )
