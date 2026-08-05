"""
Unit test scaffold for the /start command.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.bot.commands.start import aviator_promo
from app.bot.commands.start import start


@pytest.fixture
def update() -> MagicMock:
    mock_update = MagicMock()
    mock_update.message.reply_text = AsyncMock()
    mock_update.message.reply_photo = AsyncMock()
    return mock_update


@pytest.fixture
def context() -> MagicMock:
    return MagicMock()


async def test_start_sends_welcome_message_with_launch_keyboard(
    update: MagicMock, context: MagicMock
) -> None:
    await start(update, context)

    assert update.message.reply_text.await_count == 2
    # Promo photo is no longer sent by /start; it's shown after the
    # user explicitly requests the Aviator promo.
    assert update.message.reply_photo.await_count == 0

    welcome_call = update.message.reply_text.await_args_list[0]
    assert "Welcome to FanPesa" in welcome_call.kwargs["text"]
    assert welcome_call.kwargs["reply_markup"] is not None

    # aviator photo is now sent by the callback handler; see test below.


async def test_aviator_promo_callback_sends_photo(
    monkeypatch: MagicMock,
) -> None:
    mock_query = MagicMock()
    mock_query.answer = AsyncMock()
    mock_query.message = MagicMock()
    mock_query.message.chat = MagicMock()
    mock_query.message.chat.id = 123

    mock_update = MagicMock()
    mock_update.callback_query = mock_query

    mock_context = MagicMock()
    mock_context.bot.send_photo = AsyncMock()

    await aviator_promo(mock_update, mock_context)

    mock_query.answer.assert_awaited()
    assert mock_context.bot.send_photo.await_count == 1
