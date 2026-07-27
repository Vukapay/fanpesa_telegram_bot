"""
FanPesa Promotion Models
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class PromotionType(StrEnum):
    DEPOSIT_BONUS = "deposit_bonus"
    FREE_BET = "free_bet"
    CASHBACK = "cashback"
    REFERRAL = "referral"


class Promotion(BaseModel):
    """A promotional offer surfaced to users."""

    id: str
    title: str
    description: str
    type: PromotionType
    active: bool = True
    expires_at: datetime | None = None
