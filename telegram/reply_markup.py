from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)


def hr_reply_markup(user_mode: bool) -> ReplyKeyboardMarkup:
    reply_keyboard_markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=1
    )

    if user_mode:
        reply_keyboard_markup.add(
            KeyboardButton(text="I'm not HR"),
        )
    else:
        reply_keyboard_markup.add(
            KeyboardButton(text="I'm HR")
        )
    return reply_keyboard_markup


def inline_reply_markup_link(text: str, url: str) -> InlineKeyboardMarkup:
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(
        InlineKeyboardButton(
            text=text, url=url
        )
    )

    return reply_markup
