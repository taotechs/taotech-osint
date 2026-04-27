"""Bridge layer between Flask API and core OSINT engine."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import asdict, is_dataclass
import re
from typing import Any, Callable, Dict, List, TypeVar

from core.modules.domain import run_domain
from core.modules.email import run_email
from core.modules.username import run_username
from core.reporting.report_generator import CORE_REPORTS_DIR, generate_scan_report

T = TypeVar("T")
SCAN_EXECUTOR = ThreadPoolExecutor(max_workers=3)
URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")
NOISE_PATTERNS = (
    "RequestsDependencyWarning",
    "warnings.warn(",
    "UnicodeEncodeError",
    "colorama\\ansitowin32.py",
    "encodings\\cp1252.py",
    "Traceback (most recent call last):",
    "Error in worker:",
    '  File "',
)


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


def _clean_stderr(stderr_text: str) -> str:
    """Remove known noisy warnings/traceback lines from stderr output."""
    if not stderr_text:
        return ""
    if (
        "UnicodeEncodeError" in stderr_text
        or "RequestsDependencyWarning" in stderr_text
    ):
        return ""
    filtered_lines = [
        line
        for line in stderr_text.splitlines()
        if not any(pattern in line for pattern in NOISE_PATTERNS)
    ]
    return "\n".join(line for line in filtered_lines if line.strip()).strip()


def _clean_result_payload(value: Any) -> Any:
    """Recursively sanitize command results for cleaner frontend display."""
    if isinstance(value, dict):
        cleaned = {key: _clean_result_payload(item) for key, item in value.items()}
        if "stderr" in cleaned and isinstance(cleaned["stderr"], str):
            cleaned["stderr"] = _clean_stderr(cleaned["stderr"])
        return cleaned
    if isinstance(value, list):
        return [_clean_result_payload(item) for item in value]
    return value


def _extract_links(value: Any) -> List[str]:
    """Extract unique URLs from nested result payloads."""
    links: List[str] = []
    if isinstance(value, dict):
        for item in value.values():
            links.extend(_extract_links(item))
    elif isinstance(value, list):
        for item in value:
            links.extend(_extract_links(item))
    elif isinstance(value, str):
        links.extend(URL_PATTERN.findall(value))
    return list(dict.fromkeys(links))


def _build_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Build concise summary for UI cards."""
    links = _extract_links(results)
    platforms = []
    for key, value in results.items():
        if key == "target":
            continue
        if isinstance(value, dict):
            platforms.append({"name": key, "success": bool(value.get("success"))})
    success_count = sum(1 for item in platforms if item["success"])
    return {
        "platforms": platforms,
        "platforms_found": success_count,
        "links_found": len(links),
        "links": links[:20],
    }


def run_username_scan(username: str) -> Dict[str, Any]:
    """Call core username module and format API response payload."""
    raw_result = _execute_with_timeout(run_username, username, timeout_seconds=300)
    result = _clean_result_payload(_to_plain_data(raw_result))
    summary = _build_summary(result)
    generated = generate_scan_report("username", username, result)

    report_path = f"/api/reports/view/{generated['file_name']}"
    report_download_path = f"/api/reports/download/{generated['file_name']}"

    return {
        "username": username,
        "results": result,
        "report_path": report_path,
        "report_download_path": report_download_path,
        "report_created_at": generated["created_at"],
        "summary": summary,
    }


def run_email_scan(email: str) -> Dict[str, Any]:
    """Call core email module and format API response payload."""
    raw_result = _execute_with_timeout(run_email, email, timeout_seconds=240)
    result = _clean_result_payload(_to_plain_data(raw_result))
    summary = _build_summary(result)
    generated = generate_scan_report("email", email, result)
    return {
        "email": email,
        "results": result,
        "report_path": f"/api/reports/view/{generated['file_name']}",
        "report_download_path": f"/api/reports/download/{generated['file_name']}",
        "report_created_at": generated["created_at"],
        "summary": summary,
    }


def run_domain_scan(domain: str) -> Dict[str, Any]:
    """Call core domain module and format API response payload."""
    raw_result = _execute_with_timeout(run_domain, domain, timeout_seconds=420)
    result = _clean_result_payload(_to_plain_data(raw_result))
    summary = _build_summary(result)
    generated = generate_scan_report("domain", domain, result)
    return {
        "domain": domain,
        "results": result,
        "report_path": f"/api/reports/view/{generated['file_name']}",
        "report_download_path": f"/api/reports/download/{generated['file_name']}",
        "report_created_at": generated["created_at"],
        "summary": summary,
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

