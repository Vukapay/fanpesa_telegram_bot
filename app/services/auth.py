"""
Authentication Service

Resolves a platform identity (e.g. a Telegram user) to a FanPesa
`User`. Backed by the mock API until the real backend exposes an
identity/auth endpoint.
"""

from __future__ import annotations

from app.api.mock import mock_api
from app.models.user import User


class AuthService:
    """Resolves and authenticates FanPesa users across platforms."""

    async def authenticate(self, user_id: int) -> User:
        """Resolve a FanPesa `User` for the given platform user id."""
        profile = await mock_api.get_user_profile(user_id)
        return User.model_validate(profile)


auth_service = AuthService()
