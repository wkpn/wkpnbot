from aiogram import Bot
from aiogram.types import (
    ContentType,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message
)


async def edit_message(
    bot: Bot,
    chat_id: int,
    edited_message: Message,
    message_id: int
) -> None:
    """
    Helper function for editing messages of any "content_type".
    """

    caption = edited_message.md_text
    media = None

    match edited_message.content_type:
        case ContentType.TEXT:
            await bot.edit_message_text(
                text=caption,
                chat_id=chat_id,
                message_id=message_id
            )
            return
        case ContentType.VOICE:
            await bot.edit_message_caption(
                caption=caption,
                chat_id=chat_id,
                message_id=message_id
            )
            return
        case ContentType.ANIMATION:
            media = InputMediaAnimation(
                media=edited_message.animation.file_id,
                caption=caption,
                show_caption_above_media=edited_message.show_caption_above_media
            )
        case ContentType.AUDIO:
            media = InputMediaAudio(
                media=edited_message.audio.file_id,
                caption=caption
            )
        case ContentType.DOCUMENT:
            media = InputMediaDocument(
                media=edited_message.document.file_id,
                caption=caption
            )
        case ContentType.PHOTO:
            media = InputMediaPhoto(
                media=edited_message.photo[-1].file_id,
                caption=caption,
                show_caption_above_media=edited_message.show_caption_above_media
            )
        case ContentType.VIDEO:
            media = InputMediaVideo(
                media=edited_message.video.file_id,
                caption=caption,
                show_caption_above_media=edited_message.show_caption_above_media
            )

    await bot.edit_message_media(
        media=media,
        chat_id=chat_id,
        message_id=message_id
    )
