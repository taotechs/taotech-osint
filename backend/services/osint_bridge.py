"""Bridge layer between Flask API and core OSINT engine."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Dict, List, TypeVar

from core.modules.domain import run_domain
from core.modules.email import run_email
from core.modules.username import run_username
from core.reporting.report_generator import CORE_REPORTS_DIR, generate_scan_report

T = TypeVar("T")
SCAN_EXECUTOR = ThreadPoolExecutor(max_workers=3)


class OsintBridgeError(Exception):
    """Base exception for bridge-level failures."""


class OsintExecutionTimeout(OsintBridgeError):
    """Raised when an OSINT call does not complete in time."""


def _execute_with_timeout(
    task: Callable[..., T],
    *args: Any,
    timeout_seconds: int = 180,
) -> T:
    """Run a blocking OSINT task with timeout protection."""
    future = SCAN_EXECUTOR.submit(task, *args)
    try:
        return future.result(timeout=timeout_seconds)
    except FutureTimeoutError as exc:
        future.cancel()
        raise OsintExecutionTimeout(
            f"OSINT task timed out after {timeout_seconds} seconds."
        ) from exc
    except Exception as exc:
        raise OsintBridgeError(str(exc)) from exc


def _to_plain_data(value: Any) -> Any:
    """Convert dataclasses and nested structures into JSON-safe data."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _to_plain_data(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_plain_data(item) for item in value]
    return value


def run_username_scan(username: str) -> Dict[str, Any]:
    """Call core username module and format API response payload."""
    raw_result = _execute_with_timeout(run_username, username, timeout_seconds=300)
    result = _to_plain_data(raw_result)
    generated = generate_scan_report("username", username, result)

    report_path = f"/api/reports/view/{generated['file_name']}"
    report_download_path = f"/api/reports/download/{generated['file_name']}"

    return {
        "username": username,
        "results": result,
        "report_path": report_path,
        "report_download_path": report_download_path,
        "report_created_at": generated["created_at"],
    }


def run_email_scan(email: str) -> Dict[str, Any]:
    """Call core email module and format API response payload."""
    raw_result = _execute_with_timeout(run_email, email, timeout_seconds=240)
    result = _to_plain_data(raw_result)
    generated = generate_scan_report("email", email, result)
    return {
        "email": email,
        "results": result,
        "report_path": f"/api/reports/view/{generated['file_name']}",
        "report_download_path": f"/api/reports/download/{generated['file_name']}",
        "report_created_at": generated["created_at"],
    }


def run_domain_scan(domain: str) -> Dict[str, Any]:
    """Call core domain module and format API response payload."""
    raw_result = _execute_with_timeout(run_domain, domain, timeout_seconds=420)
    result = _to_plain_data(raw_result)
    generated = generate_scan_report("domain", domain, result)
    return {
        "domain": domain,
        "results": result,
        "report_path": f"/api/reports/view/{generated['file_name']}",
        "report_download_path": f"/api/reports/download/{generated['file_name']}",
        "report_created_at": generated["created_at"],
    }


def list_html_reports() -> Dict[str, List[Dict[str, str]]]:
    """List generated HTML reports from the reports directory."""
    CORE_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORE_REPORTS_DIR.glob("*.html"), reverse=True)
    reports = [
        {
            "file_name": report_file.name,
            "view_path": f"/api/reports/view/{report_file.name}",
            "download_path": f"/api/reports/download/{report_file.name}",
        }
        for report_file in files
    ]
    return {"reports": reports}

