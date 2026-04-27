"""Core username OSINT module using Maigret and Sherlock."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.utils.runner import is_tool_installed, run_command


def run_username(username: str) -> Dict[str, Any]:
    """Run username OSINT checks with Maigret and Sherlock."""
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    results: Dict[str, Any] = {
        "target": username,
        "maigret": None,
        "sherlock": None,
    }

    if is_tool_installed("maigret"):
        maigret_report = reports_dir / f"maigret_{username}.html"
        maigret_command = [
            "maigret",
            username,
            "--html",
            "--output",
            str(maigret_report),
        ]
        results["maigret"] = run_command(maigret_command)
    else:
        results["maigret"] = {
            "success": False,
            "error": "maigret is not installed or not available in PATH.",
        }

    if is_tool_installed("sherlock"):
        sherlock_command = [
            "sherlock",
            username,
            "--output",
            str(reports_dir),
        ]
        sherlock_result = run_command(sherlock_command)

        sherlock_html_report = reports_dir / f"sherlock_{username}.html"
        html_content = (
            "<html><head><meta charset='utf-8'><title>Sherlock Report</title></head>"
            "<body><h1>Sherlock Output</h1>"
            f"<h2>Username: {username}</h2>"
            "<pre>"
            f"{sherlock_result.stdout or sherlock_result.stderr or 'No output.'}"
            "</pre></body></html>"
        )
        sherlock_html_report.write_text(html_content, encoding="utf-8")
        results["sherlock"] = sherlock_result
    else:
        results["sherlock"] = {
            "success": False,
            "error": "sherlock is not installed or not available in PATH.",
        }

    return results

__all__ = ["run_username"]
