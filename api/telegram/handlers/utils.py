from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from aiogram.utils.markdown import escape_md, text as _text

from ..config import CHANNEL_ID
from ..db import deta_db


def forward_to_channel(handler):
    async def wrapped(message: Message):
        result = await handler(message)
        await message.forward(CHANNEL_ID, disable_notification=True)
        return result
    return wrapped


def inline_reply_markup_link(text: str, url: str) -> InlineKeyboardMarkup:
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(
        InlineKeyboardButton(
            text=text, url=url
        )
    )

    return reply_markup


def user_launched_bot(handler):
    async def wrapped(message: Message):
        result = await handler(message)

        from_user = message.from_user
        mention = from_user.get_mention()

        await message.bot.send_message(
            CHANNEL_ID,
            _text(
                f"Launched by {mention}",
                escape_md(f"(id={from_user.id})")
            )
        )
        return result
    return wrapped


def user_not_blocked(handler):
    async def wrapped(message: Message):
        user_id = message.from_user.id
        if deta_db.is_user_blocked(user_id):
            await message.reply("You are blocked")
        else:
            return await handler(message)
    return wrapped
