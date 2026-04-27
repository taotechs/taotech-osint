"""Input validation helpers for API query parameters."""

from __future__ import annotations

import re


USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_.-]{3,30}")
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOMAIN_PATTERN = re.compile(
    r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+"
)


def is_valid_username(username: str) -> bool:
    """Return True when the username follows supported format rules."""
    return bool(USERNAME_PATTERN.fullmatch((username or "").strip()))


def is_valid_email(email: str) -> bool:
    """Return True when the email follows common address format rules."""
    return bool(EMAIL_PATTERN.fullmatch((email or "").strip()))


def is_valid_domain(domain: str) -> bool:
    """Return True when the domain follows common hostname format rules."""
    return bool(DOMAIN_PATTERN.fullmatch((domain or "").strip().lower()))

