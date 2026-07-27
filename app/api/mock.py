"""
Mock FanPesa Backend

Simulates the responses that the real FanPesa backend API will
eventually return, so the bot and service layer can be built and
tested end-to-end before the backend team ships real endpoints.

Every method mirrors the shape a real `APIClient` call would return
(plain dicts / lists of dicts), keeping the swap to real APIs a
service-layer-only change.
"""

from __future__ import annotations

import asyncio
import random
import uuid
from datetime import UTC, datetime, timedelta

MOCK_LATENCY_SECONDS = 0.05


async def _simulate_latency() -> None:
    """Simulate realistic network latency for a mock backend call."""
    await asyncio.sleep(MOCK_LATENCY_SECONDS)


class MockAPI:
    """In-memory stand-in for the FanPesa backend API."""

    async def get_user_profile(self, user_id: int) -> dict:
        """Return a sample user profile for the given user id."""
        await _simulate_latency()

        return {
            "id": user_id,
            "username": f"fanpesa_user_{user_id}",
            "phone_number": f"+2547{random.randint(10_000_000, 99_999_999)}",
            "full_name": "FanPesa Player",
            "email": None,
            "telegram_id": user_id,
            "verified": True,
        }

    async def get_wallet_balance(self, user_id: int) -> dict:
        """Return a randomised wallet balance for demonstration purposes."""
        await _simulate_latency()

        return {
            "user_id": user_id,
            "balance": round(random.uniform(500, 50_000), 2),
            "bonus_balance": round(random.uniform(0, 2_000), 2),
            "currency": "KES",
        }

    async def get_transactions(self, user_id: int, limit: int = 10) -> list[dict]:
        """Return a sample transaction history for the given user."""
        await _simulate_latency()

        transaction_types = ["deposit", "withdrawal", "bet_placed", "bet_won", "bonus"]
        now = datetime.now(UTC)

        return [
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "type": random.choice(transaction_types),
                "amount": round(random.uniform(50, 5_000), 2),
                "status": random.choice(["completed", "completed", "completed", "pending"]),
                "currency": "KES",
                "created_at": (now - timedelta(hours=i * 3)).isoformat(),
                "description": None,
            }
            for i in range(limit)
        ]

    async def get_promotions(self) -> list[dict]:
        """Return the currently active FanPesa promotions."""
        await _simulate_latency()

        return [
            {
                "id": "promo-weekend-jackpot",
                "title": "🎉 Weekend Jackpot",
                "description": "Deposit today and get a 100% match bonus up to KES 5,000.",
                "type": "deposit_bonus",
                "active": True,
                "expires_at": None,
            },
            {
                "id": "promo-free-bet",
                "title": "🎁 Free Bet Friday",
                "description": "Place 5 bets this week and unlock a free KES 100 bet.",
                "type": "free_bet",
                "active": True,
                "expires_at": None,
            },
            {
                "id": "promo-referral",
                "title": "👥 Refer & Earn",
                "description": "Invite friends to FanPesa and earn KES 200 per referral.",
                "type": "referral",
                "active": True,
                "expires_at": None,
            },
        ]

    async def get_referral_stats(self, user_id: int) -> dict:
        """Return sample referral statistics for the given user."""
        await _simulate_latency()

        return {
            "user_id": user_id,
            "referral_code": f"FP{user_id}{random.randint(100, 999)}",
            "total_referrals": random.randint(0, 25),
            "total_earned": round(random.uniform(0, 5_000), 2),
        }

    async def heartbeat(self) -> dict:
        """Return a mock backend health/status payload."""
        await _simulate_latency()

        return {
            "status": "ok",
            "backend": "mock",
            "time": datetime.now(UTC).isoformat(),
        }


mock_api = MockAPI()
