"""
Betting Service

Betting itself happens inside the FanPesa Mini App; this service
exists so the Platform SDK and future integrations (OneApp, partner
APIs) have a consistent, typed way to read and record bet activity.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.models.bet import Bet, BetStatus


class BettingService:
    """Business-level betting operations shared across platforms."""

    async def place_bet(self, user_id: int, amount: float, odds: float) -> Bet:
        """Record a bet placed by a user."""
        if amount <= 0:
            raise ValueError("Bet amount must be greater than zero.")

        if odds <= 1:
            raise ValueError("Odds must be greater than 1.")

        return Bet(
            id=uuid.uuid4().int >> 96,
            user_id=user_id,
            amount=amount,
            odds=odds,
            status=BetStatus.PENDING,
            placed_at=datetime.now(UTC),
        )


betting_service = BettingService()
