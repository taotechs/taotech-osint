"""Core domain OSINT module using theHarvester."""

from __future__ import annotations

from typing import Any, Dict

from core.utils.runner import is_tool_installed, run_command


def run_domain(domain: str) -> Dict[str, Any]:
    """Run domain OSINT checks with theHarvester."""
    if not is_tool_installed("theHarvester"):
        return {
            "target": domain,
            "theHarvester": {
                "success": False,
                "error": "theHarvester is not installed or not available in PATH.",
            },
        }

    command = ["theHarvester", "-d", domain, "-b", "all"]
    result = run_command(command, timeout=600)
    return {"target": domain, "theHarvester": result}

__all__ = ["run_domain"]
