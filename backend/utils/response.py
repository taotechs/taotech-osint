"""Standardized JSON response helpers for Flask routes."""

from __future__ import annotations

from typing import Any, Dict, Optional

from flask import jsonify


def success_response(
    data: Dict[str, Any],
    message: str = "Success",
    status: int = 200,
):
    """Return a consistent success JSON response."""
    payload = {
        "success": True,
        "message": message,
        "status_code": status,
        "data": data,
    }
    return jsonify(payload), status


def error_response(
    message: str,
    status: int = 400,
    details: Any = None,
    error_code: Optional[str] = None,
):
    """Return a consistent error JSON response."""
    payload = {
        "success": False,
        "message": message,
        "status_code": status,
    }
    if error_code:
        payload["error_code"] = error_code
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status
