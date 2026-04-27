"""Domain OSINT API routes."""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.services.osint_bridge import (
    OsintExecutionTimeout,
    OsintBridgeError,
    run_domain_scan,
)
from backend.utils.response import error_response, success_response
from backend.utils.validators import is_valid_domain

domain_bp = Blueprint("domain_routes", __name__)


@domain_bp.get("/api/osint/domain")
def domain_scan():
    """GET /api/osint/domain?domain=xxx."""
    domain = (request.args.get("domain") or "").strip().lower()
    if not is_valid_domain(domain):
        current_app.logger.warning("Domain scan validation failed: %s", domain)
        return error_response(
            "Invalid domain format.",
            400,
            error_code="VALIDATION_ERROR",
        )

    try:
        payload = run_domain_scan(domain)
        current_app.logger.info("Domain scan completed successfully: %s", domain)
        return success_response(payload, "Domain scan completed.")
    except OsintExecutionTimeout as exc:
        current_app.logger.error("Domain scan timeout for %s: %s", domain, exc)
        return error_response(
            "Domain scan timed out.",
            504,
            details=str(exc),
            error_code="SCAN_TIMEOUT",
        )
    except OsintBridgeError as exc:
        current_app.logger.error("Domain scan service failure for %s: %s", domain, exc)
        return error_response(
            "Domain scan failed.",
            500,
            details=str(exc),
            error_code="SCAN_FAILED",
        )
