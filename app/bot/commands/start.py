"""
/start command.
"""

from __future__ import annotations

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import aviator_keyboard, launch_app_keyboard
from app.bot.keyboards.main_menu import main_menu
from app.config.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=start user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    await update.message.reply_text(
        text="""
🎉 *Welcome to FanPesa!*

The fastest betting experience inside Telegram.

✅ Register
✅ Deposit
✅ Bet
✅ Win
✅ Withdraw

👇 Tap below to get started — no need to leave Telegram.
""",
        parse_mode="Markdown",
        reply_markup=launch_app_keyboard(),
    )
    await update.message.reply_text(
        text="Use the menu below any time to jump straight to a feature.",
        reply_markup=main_menu(),
    )


async def aviator_promo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """CallbackQuery handler: send the Aviator promo when user requests it.

    This is triggered when the user taps the `Play Aviator` button on the
    launch keyboard. We answer the callback (closing the popup) and then send
    the promotional photo with a web-app button that actually opens Aviator.
    """
    query = update.callback_query
    if query is None:
        return

    try:
        await query.answer()
    except BadRequest:
        # The callback query expired before we got to it (e.g. it was
        # queued while the bot was cold-starting) — Telegram no longer
        # accepts an answer for it, but the promo photo below is still
        # useful, so keep going instead of aborting.
        # This is an expected, non-fatal condition (callback queries can
        # expire while the bot is cold-starting). Log at DEBUG to avoid
        # noisy warnings in normal operation.
        logger.debug("action=aviator_promo callback query expired, continuing anyway")

    chat = query.message.chat if query.message else update.effective_chat
    if chat is None:
        return

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=settings.aviator_image_url,
        caption="""
🔴⚫ *AVIATOR* ⚫🔴

🔥 *Our most popular game!*

Watch the multiplier climb and cash out before the plane flies away. Simple rules, fast rounds, instant payouts.

✈️ Tap below to take off.
""",
        parse_mode="Markdown",
        reply_markup=aviator_keyboard(),
    )
