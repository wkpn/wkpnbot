from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from aiogram.utils.markdown import escape_md, text

from ..config import CHANNEL_ID


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
        mention = from_user.get_mention(as_html=False)

        await message.bot.send_message(
            CHANNEL_ID,
            text(
                f"Launched by {mention}",
                escape_md(f"(id={from_user.id})")
            )
        )
        return result
    return wrapped
