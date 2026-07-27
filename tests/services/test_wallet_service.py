"""
Unit tests for `WalletService`.
"""

import pytest

from app.core.exceptions import InsufficientFundsError
from app.models.wallet import Wallet
from app.services.wallet import WalletService


@pytest.fixture
def wallet_service() -> WalletService:
    return WalletService()


async def test_get_balance_returns_wallet_model(wallet_service: WalletService) -> None:
    wallet = await wallet_service.get_balance(user_id=1)

    assert isinstance(wallet, Wallet)
    assert wallet.user_id == 1
    assert wallet.balance >= 0
    assert wallet.currency == "KES"


async def test_get_transactions_returns_typed_list(wallet_service: WalletService) -> None:
    transactions = await wallet_service.get_transactions(user_id=1, limit=3)

    assert len(transactions) == 3
    assert all(transaction.user_id == 1 for transaction in transactions)


async def test_deposit_rejects_non_positive_amount(wallet_service: WalletService) -> None:
    with pytest.raises(ValueError):
        await wallet_service.deposit(user_id=1, amount=0)


async def test_withdraw_raises_when_amount_exceeds_balance(
    wallet_service: WalletService, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def fake_get_balance(user_id: int) -> Wallet:
        return Wallet(user_id=user_id, balance=100.0, bonus_balance=0.0, currency="KES")

    monkeypatch.setattr(wallet_service, "get_balance", fake_get_balance)

    with pytest.raises(InsufficientFundsError):
        await wallet_service.withdraw(user_id=1, amount=500.0)
