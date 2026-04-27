"""Subprocess execution helpers for core OSINT tools."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CommandResult:
    """Structured result from running an external command."""

    success: bool
    command: List[str]
    return_code: Optional[int]
    stdout: str
    stderr: str
    error: Optional[str] = None


def is_tool_installed(tool_name: str) -> bool:
    """Check whether an executable is available in PATH."""
    return shutil.which(tool_name) is not None


def run_command(command: List[str], timeout: int = 300) -> CommandResult:
    """Run a command safely and return a structured result."""
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            success=process.returncode == 0,
            command=command,
            return_code=process.returncode,
            stdout=process.stdout.strip(),
            stderr=process.stderr.strip(),
        )
    except FileNotFoundError:
        return CommandResult(
            success=False,
            command=command,
            return_code=None,
            stdout="",
            stderr="",
            error=f"Command not found: {command[0]}",
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            success=False,
            command=command,
            return_code=None,
            stdout=(exc.stdout or "").strip() if exc.stdout else "",
            stderr=(exc.stderr or "").strip() if exc.stderr else "",
            error=f"Command timed out after {timeout} seconds.",
        )
    except Exception as exc:  # Defensive fallback for unexpected failures.
        return CommandResult(
            success=False,
            command=command,
            return_code=None,
            stdout="",
            stderr="",
            error=str(exc),
        )

