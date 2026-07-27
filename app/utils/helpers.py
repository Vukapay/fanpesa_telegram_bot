"""
General-purpose helper functions.
"""

from __future__ import annotations


def format_currency(amount: float, currency: str = "KES") -> str:
    """Format a numeric amount as a currency string, e.g. `KES 1,250.00`."""
    return f"{currency} {amount:,.2f}"


def mask_phone_number(phone_number: str) -> str:
    """Mask all but the last 3 digits of a phone number, e.g. `+254******789`."""
    if len(phone_number) <= 3:
        return phone_number

    visible = phone_number[-3:]
    return f"{'*' * (len(phone_number) - 3)}{visible}"


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to `max_length` characters, appending an ellipsis if cut."""
    if len(text) <= max_length:
        return text

    return f"{text[: max_length - 1]}…"
