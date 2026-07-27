"""
FanPesa Wallet Models

Typed representations of wallet balances and transactions.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET_PLACED = "bet_placed"
    BET_WON = "bet_won"
    BONUS = "bonus"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Wallet(BaseModel):
    """A snapshot of a user's wallet balance."""

    user_id: int
    balance: float
    bonus_balance: float = 0.0
    currency: str = "KES"


class Transaction(BaseModel):
    """A single wallet transaction (deposit, withdrawal, bet, bonus)."""

    id: str
    user_id: int
    type: TransactionType
    amount: float
    status: TransactionStatus
    currency: str = "KES"
    created_at: datetime
    description: str | None = None
