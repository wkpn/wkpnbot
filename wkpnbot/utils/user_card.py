import secrets

from aiogram import Bot, md
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.link import (
    create_telegram_link,
    create_tg_link
)

from .callbacks import UserUpdateCallback
from .defaults import DEFAULT_PHOTO


def build_user_card_keyboard(
    user_id: int,
    user_link: str | None = None
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

    if user_link:
        builder.button(url=user_link, text="🪪 Profile")

    return builder.as_markup()


async def prepare_user_card_info(bot: Bot, user_id: int) -> tuple[str, str, str | None, str]:
    user_info = await bot.get_chat(user_id)
    user_photos = await bot.get_user_profile_photos(user_id, limit=1)

    caption = f"👤 {md.bold(md.quote(user_info.full_name))}\n\n"

    if bio := user_info.bio:
        caption += f"📝 {md.italic(md.quote(bio))}\n\n"

    if user_info.has_restricted_voice_and_video_messages:
        caption += md.blockquote("🔇 User restricted receiving of voice/video messages")
    else:
        caption += md.blockquote("🔈 You can send voice or video messages to this user")

    caption += f"\n\n\n🆔 {md.code(user_id)}"

    if photos := user_photos.photos:
        photo = photos[0][-1].file_id
    else:
        photo = DEFAULT_PHOTO

    link_to_user_profile = None

    if username := user_info.username:
        link_to_user_profile = create_telegram_link(username)
    elif not user_info.has_private_forwards:
        link_to_user_profile = create_tg_link("user", id=user_id)

    return photo, caption, link_to_user_profile, user_info.full_name
