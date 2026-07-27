"""
Platform SDK — Telegram Adapter

Implements `PlatformAdapter` for the Telegram Mini App / bot client.
This is the only module in the bot layer that is allowed to depend
on both `telegram` and the service layer at the same time — bot
commands and handlers must go through this adapter instead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.constants import Platform
from app.core.logger import get_logger
from app.models.bet import Bet
from app.models.promotion import Promotion
from app.models.user import User
from app.models.wallet import Transaction, Wallet
from app.platform.base import PlatformAdapter, PlatformIdentity
from app.services.auth import auth_service
from app.services.betting import betting_service
from app.services.notification import notification_service
from app.services.promotion import promotion_service
from app.services.referral import referral_service
from app.services.wallet import wallet_service

if TYPE_CHECKING:
    from telegram import Bot

logger = get_logger(__name__)


class TelegramAdapter(PlatformAdapter):
    """Adapts the shared FanPesa service layer to the Telegram platform."""

    platform = Platform.TELEGRAM

    def __init__(self, bot: Bot | None = None) -> None:
        # `bot` is optional so the adapter can be used outside of a live
        # polling/webhook context (e.g. in tests or background jobs).
        self._bot = bot

    async def authenticate(self, identity: PlatformIdentity) -> User:
        return await auth_service.authenticate(int(identity.external_id))

    async def get_wallet_balance(self, user_id: int) -> Wallet:
        return await wallet_service.get_balance(user_id)

    async def get_transaction_history(self, user_id: int) -> list[Transaction]:
        return await wallet_service.get_transactions(user_id)

    async def place_bet(self, user_id: int, amount: float, odds: float) -> Bet:
        return await betting_service.place_bet(user_id, amount, odds)

    async def list_promotions(self) -> list[Promotion]:
        return await promotion_service.list_active()

    async def get_referral_code(self, user_id: int) -> str:
        return await referral_service.get_referral_code(user_id)

    async def get_referral_stats(self, user_id: int) -> dict:
        return await referral_service.get_referral_stats(user_id)

    async def send_notification(self, user_id: int, message: str) -> None:
        await notification_service.notify(user_id, message)

        if self._bot is not None:
            await self._bot.send_message(chat_id=user_id, text=message)
        else:
            logger.warning("TelegramAdapter has no bot instance; message not delivered.")


telegram_adapter = TelegramAdapter()
