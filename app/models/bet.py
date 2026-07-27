"""
FanPesa Bet Models
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class BetStatus(StrEnum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    VOID = "void"


class Bet(BaseModel):
    """A single bet placed through the FanPesa Mini App."""

    id: int
    user_id: int
    amount: float
    odds: float
    status: BetStatus = BetStatus.PENDING
    placed_at: datetime | None = None

    @property
    def potential_payout(self) -> float:
        """Amount returned to the user if this bet wins."""
        return round(self.amount * self.odds, 2)
