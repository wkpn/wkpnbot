from aiogram import Dispatcher
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from aiogram.utils.markdown import escape_md, text

from ..config import channel_id


def forward_to_channel(handler):
    async def wrapped(message: Message):
        result = await handler(message)
        await message.forward(channel_id, disable_notification=True)
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


async def user_launched_bot(dp: Dispatcher, mention: str, user_id: int):
    await dp.bot.send_message(
        channel_id,
        text(
            f"Launched by {mention}",
            escape_md(f"(id={user_id})")
        )
    )
