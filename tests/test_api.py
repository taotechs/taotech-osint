"""API integration tests for Taotech OSINT Flask backend.

These tests mock service calls so no real OSINT scan tools are executed.
"""

from __future__ import annotations

import pytest

from backend.app import create_app
from backend.services.osint_service import OsintExecutionTimeout, OsintServiceError


SAMPLE_USERNAME = "john_doe"
SAMPLE_EMAIL = "john@example.com"
SAMPLE_DOMAIN = "example.com"


@pytest.fixture()
def client():
    """Create Flask test client for API tests."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_check_endpoint(client):
    """Health endpoint returns standardized success payload."""
    response = client.get("/api/health")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["status_code"] == 200
    assert payload["data"]["status"] == "ok"


def test_username_search_success(client, monkeypatch):
    """Username endpoint returns expected JSON shape on success."""

    def fake_scan(_username):
        return {
            "username": SAMPLE_USERNAME,
            "results": {"target": SAMPLE_USERNAME, "maigret": {}, "sherlock": {}},
            "report_path": "/reports/maigret_john_doe.html",
        }

    monkeypatch.setattr("backend.routes.username_routes.run_username_scan", fake_scan)

    response = client.get(f"/api/osint/username?username={SAMPLE_USERNAME}")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["username"] == SAMPLE_USERNAME
    assert "results" in payload["data"]
    assert "report_path" in payload["data"]


def test_email_search_success(client, monkeypatch):
    """Email endpoint returns structured JSON on success."""

    def fake_scan(_email):
        return {
            "email": SAMPLE_EMAIL,
            "results": {"target": SAMPLE_EMAIL, "holehe": {"success": True}},
        }

    monkeypatch.setattr("backend.routes.email_routes.run_email_scan", fake_scan)

    response = client.get(f"/api/osint/email?email={SAMPLE_EMAIL}")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["email"] == SAMPLE_EMAIL
    assert "results" in payload["data"]


def test_domain_search_success(client, monkeypatch):
    """Domain endpoint returns structured JSON on success."""

    def fake_scan(_domain):
        return {
            "domain": SAMPLE_DOMAIN,
            "results": {
                "target": SAMPLE_DOMAIN,
                "theHarvester": {"success": True},
            },
        }

    monkeypatch.setattr("backend.routes.domain_routes.run_domain_scan", fake_scan)

    response = client.get(f"/api/osint/domain?domain={SAMPLE_DOMAIN}")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["domain"] == SAMPLE_DOMAIN
    assert "results" in payload["data"]


def test_username_validation_error(client):
    """Invalid username returns validation error payload."""
    response = client.get("/api/osint/username?username=a")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error_code"] == "VALIDATION_ERROR"


def test_email_validation_error(client):
    """Invalid email returns validation error payload."""
    response = client.get("/api/osint/email?email=not-an-email")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error_code"] == "VALIDATION_ERROR"


def test_domain_validation_error(client):
    """Invalid domain returns validation error payload."""
    response = client.get("/api/osint/domain?domain=bad_domain")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error_code"] == "VALIDATION_ERROR"


def test_scan_timeout_error(client, monkeypatch):
    """Service timeout maps to API 504 response."""

    def fake_scan(_username):
        raise OsintExecutionTimeout("timed out")

    monkeypatch.setattr("backend.routes.username_routes.run_username_scan", fake_scan)

    response = client.get(f"/api/osint/username?username={SAMPLE_USERNAME}")
    payload = response.get_json()

    assert response.status_code == 504
    assert payload["success"] is False
    assert payload["error_code"] == "SCAN_TIMEOUT"


def test_scan_failure_error(client, monkeypatch):
    """Service failure maps to API 500 response."""

    def fake_scan(_email):
        raise OsintServiceError("scan failed")

    monkeypatch.setattr("backend.routes.email_routes.run_email_scan", fake_scan)

    response = client.get(f"/api/osint/email?email={SAMPLE_EMAIL}")
    payload = response.get_json()

    assert response.status_code == 500
    assert payload["success"] is False
    assert payload["error_code"] == "SCAN_FAILED"
