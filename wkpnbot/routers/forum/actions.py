from contextlib import suppress
from typing import NoReturn

from aiogram import Bot, F, Router
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError
)
from aiogram.types import (
    CallbackQuery,
    InputMediaPhoto,
    Message,
    MessageReactionUpdated,
    ReplyParameters
)

from ..edit_message import edit_message
from ...utils import (
    UserUpdateCallback,
    build_user_card_keyboard,
    prepare_user_card_info
)


def build_forum_actions_router(forum_id: int) -> Router:
    """
    All forum interactions take place here.
    Forum admin can send a message (can be forwarded, can be a reply, can contain media, etc.).
    Forum admin can edit an already sent message.
    Forum admin can react to any message in the forum topic with the user.
    Forum admin can also update user's card with the most recent information about the user.
    """

    router = Router(name="forum.actions")

    router.callback_query.filter(F.message.chat.id == forum_id)
    router.edited_message.filter(F.chat.id == forum_id)
    router.message.filter(F.chat.id == forum_id)
    router.message_reaction.filter(F.chat.id == forum_id)

    @router.message()
    async def handle_message_in_forum(
        message: Message,
        forum_topic_record: dict[str, int],
        reply_parameters: ReplyParameters | None = None
    ) -> tuple[int, int]:
        user_chat_id = forum_topic_record["chat_id"]

        if message.forward_origin:
            sent_to_user = await message.forward(
                chat_id=user_chat_id
            )
        else:
            sent_to_user = await message.copy_to(
                chat_id=user_chat_id,
                reply_parameters=reply_parameters
            )

        return sent_to_user.message_id, message.message_id

    @router.edited_message()
    async def handle_edited_message_in_forum(
        edited_message: Message,
        bot: Bot,
        messages_record: dict[str, int]
    ) -> NoReturn:
        user_chat_id = messages_record["user_chat_id"]
        user_chat_message_id = messages_record["user_chat_message_id"]

        with suppress(TelegramForbiddenError):
            await edit_message(
                bot=bot,
                chat_id=user_chat_id,
                edited_message=edited_message,
                message_id=user_chat_message_id
            )

    @router.callback_query(
        UserUpdateCallback.filter(F.type == "update")
    )
    async def handle_user_card_update_in_forum(
        callback_query: CallbackQuery,
        callback_data: UserUpdateCallback,
        bot: Bot
    ) -> NoReturn:
        await callback_query.answer(text="🔄 Updating user data...")

        user_id = callback_data.user_id
        message = callback_query.message

        photo, caption, user_link, user_full_name = await prepare_user_card_info(
            bot, user_id
        )
        reply_markup = build_user_card_keyboard(user_id, user_link)

        await message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=reply_markup
        )

        with suppress(TelegramBadRequest):
            await bot.edit_forum_topic(
                chat_id=forum_id,
                message_thread_id=message.message_thread_id,
                name=user_full_name
            )

    @router.message_reaction()
    async def handle_message_reaction_in_forum(
        message_reaction: MessageReactionUpdated,
        bot: Bot,
        messages_record: dict[str, int]
    ) -> NoReturn:
        admin_reaction = message_reaction.new_reaction

        user_chat_id = messages_record["user_chat_id"]
        user_chat_message_id = messages_record["user_chat_message_id"]

        await bot.set_message_reaction(
            chat_id=user_chat_id,
            message_id=user_chat_message_id,
            reaction=admin_reaction,
            is_big=True
        )

    return router
