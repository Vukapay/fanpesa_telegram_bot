"""
Referral Service

Provides referral codes, invite links, and referral statistics,
backed by the mock API until the real referral backend is available.
"""

from __future__ import annotations

from app.api.mock import mock_api
from app.core.constants import BOT_USERNAME


class ReferralService:
    """Business-level referral operations used by every platform adapter."""

    async def get_referral_code(self, user_id: int) -> str:
        """Return a user's unique referral code."""
        stats = await mock_api.get_referral_stats(user_id)
        return stats["referral_code"]

    async def get_referral_stats(self, user_id: int) -> dict:
        """Return referral statistics (total referrals, total earned) for a user."""
        return await mock_api.get_referral_stats(user_id)

    async def build_invite_link(self, user_id: int) -> str:
        """Build a Telegram deep link that credits the referring user."""
        code = await self.get_referral_code(user_id)
        return f"https://t.me/{BOT_USERNAME}?start=ref_{code}"


referral_service = ReferralService()
