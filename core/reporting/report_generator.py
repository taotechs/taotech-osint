"""Generate structured HTML reports from OSINT scan outputs."""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


CORE_REPORTS_DIR = Path("core") / "reports"
URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")


def _extract_links(value: Any) -> List[str]:
    """Recursively extract URLs from nested result objects."""
    links: List[str] = []

    if isinstance(value, dict):
        for item in value.values():
            links.extend(_extract_links(item))
    elif isinstance(value, list):
        for item in value:
            links.extend(_extract_links(item))
    elif isinstance(value, str):
        links.extend(URL_PATTERN.findall(value))

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(links))


def _extract_platforms(results: Dict[str, Any]) -> List[Tuple[str, bool]]:
    """Extract platform/tool status rows from known result keys."""
    platforms: List[Tuple[str, bool]] = []
    for key, value in results.items():
        if key == "target":
            continue
        success = False
        if isinstance(value, dict):
            success = bool(value.get("success"))
        platforms.append((key, success))
    return platforms


def _render_html_report(
    report_title: str,
    target: str,
    results: Dict[str, Any],
    timestamp: str,
) -> str:
    """Render a styled HTML report string."""
    platforms = _extract_platforms(results)
    links = _extract_links(results)
    escaped_json = html.escape(str(results))

    platform_rows = "".join(
        [
            (
                f"<tr><td>{html.escape(name)}</td>"
                f"<td>{'Found' if found else 'Not found'}</td></tr>"
            )
            for name, found in platforms
        ]
    ) or "<tr><td colspan='2'>No platform data available</td></tr>"

    link_rows = "".join(
        [
            (
                "<li><a href='{0}' target='_blank' rel='noreferrer'>{0}</a></li>".format(
                    html.escape(link)
                )
            )
            for link in links
        ]
    ) or "<li>No links detected in this scan output.</li>"

    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(report_title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 24px; background: #0b1220; color: #e2e8f0; }}
    .card {{ background: #111a2e; border: 1px solid #233252; border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
    h1, h2 {{ color: #67e8f9; margin: 0 0 12px 0; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #233252; padding: 8px; text-align: left; }}
    th {{ background: #16233d; }}
    a {{ color: #22d3ee; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #0f172a; padding: 12px; border-radius: 8px; }}
    .meta {{ color: #93c5fd; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{html.escape(report_title)}</h1>
    <p class="meta"><strong>Target:</strong> {html.escape(target)}</p>
    <p class="meta"><strong>Generated:</strong> {html.escape(timestamp)}</p>
  </div>

  <div class="card">
    <h2>Platforms Found</h2>
    <table>
      <thead><tr><th>Platform/Tool</th><th>Status</th></tr></thead>
      <tbody>{platform_rows}</tbody>
    </table>
  </div>

  <div class="card">
    <h2>Links and Results</h2>
    <ul>{link_rows}</ul>
  </div>

  <div class="card">
    <h2>Raw Result Snapshot</h2>
    <pre>{escaped_json}</pre>
  </div>
</body>
</html>
"""


def generate_scan_report(
    scan_type: str,
    target: str,
    results: Dict[str, Any],
) -> Dict[str, str]:
    """Create and persist a structured HTML report for a scan."""
    CORE_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    safe_target = re.sub(r"[^a-zA-Z0-9_.-]+", "_", target).strip("_") or "target"
    file_name = (
        f"{scan_type}_{safe_target}_"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.html"
    )

    report_title = f"Taotech OSINT {scan_type.title()} Report"
    report_html = _render_html_report(report_title, target, results, timestamp)

    report_path = CORE_REPORTS_DIR / file_name
    report_path.write_text(report_html, encoding="utf-8")

    return {
        "file_name": file_name,
        "created_at": timestamp,
    }

