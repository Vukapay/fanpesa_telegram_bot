"""
Platform SDK — Safaricom OneApp Adapter

Implements `PlatformAdapter` for a future Safaricom OneApp
integration. Delegates to the exact same service layer as the
Telegram and browser adapters — only the identity resolution and
notification transport will differ once OneApp's real APIs exist.
"""

from __future__ import annotations

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

logger = get_logger(__name__)


class OneAppAdapter(PlatformAdapter):
    """Adapts the shared FanPesa service layer to the Safaricom OneApp platform."""

    platform = Platform.ONEAPP

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
        # Real delivery will use the Safaricom OneApp notification API.
        await notification_service.notify(user_id, message)
        logger.info("OneApp notification transport not yet implemented; logged only.")


oneapp_adapter = OneAppAdapter()
