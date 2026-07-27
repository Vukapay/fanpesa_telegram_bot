"""
Wallet Service

Provides wallet balance and transaction history, backed by the mock
API until the real FanPesa wallet backend is available.
"""

from __future__ import annotations

from app.api.mock import mock_api
from app.core.exceptions import InsufficientFundsError
from app.models.wallet import Transaction, Wallet


class WalletService:
    """Business-level wallet operations used by every platform adapter."""

    async def get_balance(self, user_id: int) -> Wallet:
        """Return the current wallet balance for a user."""
        data = await mock_api.get_wallet_balance(user_id)
        return Wallet.model_validate(data)

    async def get_transactions(self, user_id: int, limit: int = 10) -> list[Transaction]:
        """Return recent wallet transactions for a user."""
        data = await mock_api.get_transactions(user_id, limit=limit)
        return [Transaction.model_validate(item) for item in data]

    async def deposit(self, user_id: int, amount: float) -> Wallet:
        """Deposit funds into a user's wallet."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        # NOTE: the mock backend has no persistence, so this returns a
        # freshly generated balance rather than an incremented one.
        # Real deposits will be handled by the FanPesa backend.
        return await self.get_balance(user_id)

    async def withdraw(self, user_id: int, amount: float) -> Wallet:
        """Withdraw funds from a user's wallet."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        wallet = await self.get_balance(user_id)

        if amount > wallet.balance:
            raise InsufficientFundsError(
                f"Withdrawal of {amount} exceeds available balance of {wallet.balance}."
            )

        return wallet


wallet_service = WalletService()
