"""Core module tests with mocked OSINT command execution."""

from __future__ import annotations

from core.modules.domain import run_domain
from core.modules.email import run_email
from core.modules.username import run_username
from core.utils.runner import CommandResult


SAMPLE_USERNAME = "alice_sec"
SAMPLE_EMAIL = "alice@example.com"
SAMPLE_DOMAIN = "example.org"


def _fake_command_result(stdout: str = "ok") -> CommandResult:
    """Create reusable mocked command result."""
    return CommandResult(
        success=True,
        command=["mocked"],
        return_code=0,
        stdout=stdout,
        stderr="",
        error=None,
    )


def test_run_username_success_with_mocked_tools(monkeypatch, tmp_path):
    """Username module should return tool results and generate HTML output."""

    def fake_is_tool_installed(_tool):
        return True

    def fake_run_command(command, timeout=300):  # noqa: ARG001
        if command[0] == "sherlock":
            return _fake_command_result(stdout="https://twitter.com/alice_sec")
        return _fake_command_result(stdout="maigret finished")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("core.modules.username.is_tool_installed", fake_is_tool_installed)
    monkeypatch.setattr("core.modules.username.run_command", fake_run_command)

    result = run_username(SAMPLE_USERNAME)

    assert result["target"] == SAMPLE_USERNAME
    assert result["maigret"].success is True
    assert result["sherlock"].success is True
    assert (tmp_path / "reports" / f"sherlock_{SAMPLE_USERNAME}.html").exists()


def test_run_username_handles_missing_tools(monkeypatch, tmp_path):
    """Username module should gracefully handle missing tool binaries."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("core.modules.username.is_tool_installed", lambda _tool: False)

    result = run_username(SAMPLE_USERNAME)

    assert result["maigret"]["success"] is False
    assert result["sherlock"]["success"] is False


def test_run_email_success_with_mocked_tool(monkeypatch):
    """Email module should return structured success result."""
    monkeypatch.setattr("core.modules.email.is_tool_installed", lambda _tool: True)
    monkeypatch.setattr(
        "core.modules.email.run_command",
        lambda _command: _fake_command_result(stdout="GitHub: found"),
    )

    result = run_email(SAMPLE_EMAIL)

    assert result["target"] == SAMPLE_EMAIL
    assert result["holehe"].success is True


def test_run_email_missing_tool(monkeypatch):
    """Email module should return clean error when holehe is missing."""
    monkeypatch.setattr("core.modules.email.is_tool_installed", lambda _tool: False)

    result = run_email(SAMPLE_EMAIL)

    assert result["target"] == SAMPLE_EMAIL
    assert result["holehe"]["success"] is False


def test_run_domain_success_with_mocked_tool(monkeypatch):
    """Domain module should return structured success result."""
    monkeypatch.setattr("core.modules.domain.is_tool_installed", lambda _tool: True)
    monkeypatch.setattr(
        "core.modules.domain.run_command",
        lambda _command, timeout=600: _fake_command_result(stdout="DNS data"),
    )

    result = run_domain(SAMPLE_DOMAIN)

    assert result["target"] == SAMPLE_DOMAIN
    assert result["theHarvester"].success is True


def test_run_domain_missing_tool(monkeypatch):
    """Domain module should return clean error when theHarvester is missing."""
    monkeypatch.setattr("core.modules.domain.is_tool_installed", lambda _tool: False)

    result = run_domain(SAMPLE_DOMAIN)

    assert result["target"] == SAMPLE_DOMAIN
    assert result["theHarvester"]["success"] is False
