"""
FanPesa User Models

Represents a FanPesa account and the platform-specific identity
attached to it (currently Telegram, later browser/OneApp).
"""

from __future__ import annotations

from pydantic import BaseModel


class TelegramProfile(BaseModel):
    """Telegram-specific identity attached to a FanPesa account."""

    telegram_id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    language_code: str | None = None


class User(BaseModel):
    """A FanPesa user profile, as returned by the backend/mock API."""

    id: int
    username: str
    phone_number: str | None = None
    full_name: str | None = None
    email: str | None = None
    telegram_id: int | None = None
    verified: bool = False
