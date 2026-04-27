"""Taotech OSINT Toolkit entry point."""

from __future__ import annotations

import re
from dataclasses import asdict, is_dataclass
from typing import Any, Dict

from core.modules.domain import run_domain
from core.modules.email import run_email
from core.modules.username import run_username
from core.utils.logger import setup_logger


def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", username))


def is_valid_email(email: str) -> bool:
    """Validate basic email format."""
    return bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email))


def is_valid_domain(domain: str) -> bool:
    """Validate basic domain format."""
    return bool(
        re.fullmatch(
            r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+",
            domain,
        )
    )


def to_plain_data(value: Any) -> Any:
    """Convert dataclass objects to dictionaries for clean display."""
    if is_dataclass(value):
        return asdict(value)
    return value


def print_result_block(title: str, result: Any) -> None:
    """Print tool results in a readable and beginner-friendly format."""
    data = to_plain_data(result)
    print(f"\n--- {title} ---")

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(data)


def display_scan_result(scan_type: str, result: Dict[str, Any]) -> None:
    """Display formatted result sections for a scan operation."""
    print("\n========================================")
    print(f"{scan_type.upper()} SCAN RESULT")
    print("========================================")

    for key, value in result.items():
        if key == "target":
            print(f"target: {value}")
            continue
        print_result_block(key, value)

    print("\nScan complete.\n")


def menu() -> None:
    """Render interactive menu and process user choices."""
    logger = setup_logger("logs.txt")

    while True:
        print("==== Taotech OSINT Toolkit ====")
        print("1. Username Search")
        print("2. Email Search")
        print("3. Domain Search")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        try:
            if choice == "1":
                username = input("Enter username: ").strip()
                if not is_valid_username(username):
                    print(
                        "Invalid username. Use 3-30 chars: letters, numbers, _, ., -"
                    )
                    continue

                logger.info("Starting username scan for target: %s", username)
                result = run_username(username)
                display_scan_result("username", result)
                logger.info("Finished username scan for target: %s", username)

            elif choice == "2":
                email = input("Enter email: ").strip()
                if not is_valid_email(email):
                    print("Invalid email format.")
                    continue

                logger.info("Starting email scan for target: %s", email)
                result = run_email(email)
                display_scan_result("email", result)
                logger.info("Finished email scan for target: %s", email)

            elif choice == "3":
                domain = input("Enter domain (example.com): ").strip().lower()
                if not is_valid_domain(domain):
                    print("Invalid domain format.")
                    continue

                logger.info("Starting domain scan for target: %s", domain)
                result = run_domain(domain)
                display_scan_result("domain", result)
                logger.info("Finished domain scan for target: %s", domain)

            elif choice == "4":
                print("Exiting Taotech OSINT Toolkit. Goodbye!")
                logger.info("Application closed by user.")
                break

            else:
                print("Invalid option. Please choose 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\nOperation interrupted by user.")
            logger.warning("Operation interrupted by user (KeyboardInterrupt).")
        except Exception as exc:
            print(f"Unexpected error: {exc}")
            logger.exception("Unhandled error occurred: %s", exc)


if __name__ == "__main__":
    menu()
