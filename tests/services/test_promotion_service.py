"""
Unit tests for `PromotionService`.
"""

import pytest

from app.models.promotion import Promotion
from app.services.promotion import PromotionService


@pytest.fixture
def promotion_service() -> PromotionService:
    return PromotionService()


async def test_list_active_returns_only_active_promotions(
    promotion_service: PromotionService,
) -> None:
    promotions = await promotion_service.list_active()

    assert promotions
    assert all(isinstance(promotion, Promotion) for promotion in promotions)
    assert all(promotion.active for promotion in promotions)
