"""
Security utilities.

NOTE:
Authentication will ultimately be handled by the backend.
This module provides reusable cryptographic helpers.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Final

TOKEN_LENGTH: Final[int] = 32


def generate_secret(length: int = TOKEN_LENGTH) -> str:
    """Generate a secure random secret."""
    return secrets.token_hex(length)


def sha256(data: str) -> str:
    """Return SHA256 hash."""
    return hashlib.sha256(data.encode()).hexdigest()


def verify_signature(secret: str, payload: str, signature: str) -> bool:
    """Verify HMAC SHA256 signature."""
    digest = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(digest, signature)


def constant_compare(value1: str, value2: str) -> bool:
    """Timing-safe comparison."""
    return hmac.compare_digest(value1, value2)
