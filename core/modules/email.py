"""Core email OSINT module using Holehe."""

from __future__ import annotations

from typing import Any, Dict

from core.utils.runner import is_tool_installed, run_command


def run_email(email: str) -> Dict[str, Any]:
    """Run email OSINT checks with Holehe."""
    if not is_tool_installed("holehe"):
        return {
            "target": email,
            "holehe": {
                "success": False,
                "error": "holehe is not installed or not available in PATH.",
            },
        }

    command = ["holehe", email, "--only-used"]
    result = run_command(command)
    return {"target": email, "holehe": result}

__all__ = ["run_email"]
