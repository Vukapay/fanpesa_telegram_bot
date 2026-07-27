"""
Promotion Service

Surfaces active FanPesa promotions, backed by the mock API until the
real promotions backend is available.
"""

from __future__ import annotations

from app.api.mock import mock_api
from app.models.promotion import Promotion


class PromotionService:
    """Business-level promotion operations used by every platform adapter."""

    async def list_active(self) -> list[Promotion]:
        """Return currently active promotions."""
        data = await mock_api.get_promotions()
        promotions = [Promotion.model_validate(item) for item in data]
        return [promotion for promotion in promotions if promotion.active]


promotion_service = PromotionService()
