"""
Unit test scaffold for the /start command.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

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
    assert update.message.reply_photo.await_count == 1

    welcome_call = update.message.reply_text.await_args_list[0]
    assert "Welcome to FanPesa" in welcome_call.kwargs["text"]
    assert welcome_call.kwargs["reply_markup"] is not None

    aviator_call = update.message.reply_photo.await_args_list[0]
    assert "AVIATOR" in aviator_call.kwargs["caption"]
    assert aviator_call.kwargs["reply_markup"] is not None
