"""Compatibility layer that re-exports bridge services."""

from backend.services.osint_bridge import (
    OsintBridgeError as OsintServiceError,
    OsintExecutionTimeout,
    list_html_reports,
    run_domain_scan,
    run_email_scan,
    run_username_scan,
)

__all__ = [
    "OsintExecutionTimeout",
    "OsintServiceError",
    "list_html_reports",
    "run_username_scan",
    "run_email_scan",
    "run_domain_scan",
]
