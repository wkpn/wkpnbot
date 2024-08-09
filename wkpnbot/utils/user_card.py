from aiogram import (
    Bot,
    md
)
from aiogram.utils.link import (
    create_telegram_link,
    create_tg_link
)

from .defaults import DEFAULT_PHOTO


def _join(*strings: str, times: int = 2) -> str:
    return ("\n" * times).join(strings)


async def make_user_card_info(
    bot: Bot,
    user_id: int
) -> tuple[str, str, str | None, str]:
    short_info = []

    user_info = await bot.get_chat(user_id)

    full_name = user_info.full_name
    short_info.append(f"👤 {md.bold(md.quote(full_name))}")

    if bio := user_info.bio:
        short_info.append(f"📝 {md.italic(md.quote(bio))}")

    if user_info.has_restricted_voice_and_video_messages:
        short_info.append(
            md.blockquote("🔇 User restricted receiving of voice/video messages")
        )
    else:
        short_info.append(
            md.blockquote("🔈 You can send voice or video messages to this user")
        )

    code_user_id = f"🆔 {md.code(user_id)}"

    caption = _join(_join(*short_info), code_user_id, times=3)

    user_photos = await bot.get_user_profile_photos(user_id, limit=1)

    if photos := user_photos.photos:
        photo = photos[0][-1].file_id
    else:
        photo = DEFAULT_PHOTO

    tg_link = None

    if username := user_info.username:
        tg_link = create_telegram_link(username)
    elif not user_info.has_private_forwards:
        tg_link = create_tg_link("user", id=user_id)

    return photo, caption, tg_link, full_name
