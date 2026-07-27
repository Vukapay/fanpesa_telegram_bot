"""
Platform SDK — Base Interfaces

Defines the platform-agnostic contract that every FanPesa client
integration (Telegram, browser, Safaricom OneApp, future partners)
must implement. Bot commands, web routes, and OneApp handlers all
depend on this interface — never on a concrete platform module or
on the service layer directly.

Adding a new platform means writing one adapter class here; no
changes to the service layer or business logic are required.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.constants import Platform
from app.models.bet import Bet
from app.models.promotion import Promotion
from app.models.user import User
from app.models.wallet import Transaction, Wallet


class PlatformIdentity:
    """The identity of a user as seen by a specific platform."""

    def __init__(
        self,
        external_id: str,
        display_name: str | None = None,
        username: str | None = None,
    ) -> None:
        self.external_id = external_id
        self.display_name = display_name
        self.username = username


class PlatformAdapter(ABC):
    """
    Abstract base class for a FanPesa platform integration.

    Concrete adapters (`TelegramAdapter`, `BrowserAdapter`,
    `OneAppAdapter`) translate platform-specific requests into calls
    against the shared service layer, and normalize the responses
    back into platform-friendly shapes.
    """

    platform: Platform

    @abstractmethod
    async def authenticate(self, identity: PlatformIdentity) -> User:
        """Resolve or create a FanPesa user for this platform identity."""

    @abstractmethod
    async def get_wallet_balance(self, user_id: int) -> Wallet:
        """Return the current wallet balance for a user."""

    @abstractmethod
    async def get_transaction_history(self, user_id: int) -> list[Transaction]:
        """Return recent wallet transactions for a user."""

    @abstractmethod
    async def place_bet(self, user_id: int, amount: float, odds: float) -> Bet:
        """Place a bet on behalf of a user."""

    @abstractmethod
    async def list_promotions(self) -> list[Promotion]:
        """Return currently active promotions."""

    @abstractmethod
    async def get_referral_code(self, user_id: int) -> str:
        """Return a user's referral code."""

    @abstractmethod
    async def get_referral_stats(self, user_id: int) -> dict:
        """Return a user's referral statistics (total referrals, total earned)."""

    @abstractmethod
    async def send_notification(self, user_id: int, message: str) -> None:
        """Deliver a notification to a user through this platform."""
