import secrets

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import (
    EditedMessageCallback,
    UserUpdateCallback
)
from .defaults import DEFAULT_PRIVACY_POLICY_LINK


def build_edited_message_keyboard(
    edit_date: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✍️",
        callback_data=EditedMessageCallback(
            type="edited",
            edit_date=edit_date
        )
    )

    return builder.as_markup()


def build_privacy_policy_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔒 Privacy Policy",
        url=DEFAULT_PRIVACY_POLICY_LINK
    )

    return builder.as_markup()


def build_user_card_keyboard(
    user_id: int,
    tg_link: str | None = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔄 Update",
        callback_data=UserUpdateCallback(
            type="update",
            user_id=user_id,
            random_data=secrets.token_hex(8)
        )
    )

    if tg_link:
        builder.button(text="🪪 Profile", url=tg_link)

    return builder.as_markup()
