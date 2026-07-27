"""
Input validation helpers.
"""

from __future__ import annotations

import re

PHONE_NUMBER_PATTERN = re.compile(r"^\+254[17]\d{8}$")


def validate_phone_number(phone_number: str) -> bool:
    """Validate a Kenyan phone number in `+2547XXXXXXXX` / `+2541XXXXXXXX` format."""
    return bool(PHONE_NUMBER_PATTERN.match(phone_number))


def validate_amount(amount: float, minimum: float = 1.0) -> bool:
    """Validate that a monetary amount is a positive number above `minimum`."""
    return amount >= minimum


def validate_odds(odds: float) -> bool:
    """Validate that betting odds are greater than 1.0."""
    return odds > 1.0
