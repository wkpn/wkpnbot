from contextlib import suppress

from aiogram import (
    Bot,
    F,
    Router
)
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError
)
from aiogram.types import (
    CallbackQuery,
    InputMediaPhoto,
    Message,
    MessageReactionUpdated,
    ReactionTypeCustomEmoji,
    ReplyParameters
)

from ..common import (
    attach_view_edited_message_edit_date_handler,
    edit_message

)
from ...db import DBClient
from ...utils import (
    TRASH_EMOJI_ID,
    UserUpdateCallback,
    WipeForumTopicCallback,
    build_user_card_keyboard,
    make_user_card_info
)


def build_forum_actions_router(
    forum_id: int,
    messages_table: str,
    topics_table: str
) -> Router:
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
        forum_topic_record: dict[str, int | str],
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
        messages_record: dict[str, int | str]
    ) -> None:
        user_chat_id = messages_record["user_chat_id"]
        user_chat_message_id = messages_record["user_chat_message_id"]

        with suppress(TelegramForbiddenError):
            await edit_message(
                bot=bot,
                chat_id=user_chat_id,
                edited_message=edited_message,
                message_id=user_chat_message_id
            )

    attach_view_edited_message_edit_date_handler(router)

    @router.callback_query(
        UserUpdateCallback.filter(F.type == "update")
    )
    async def handle_user_card_update_in_forum(
        callback_query: CallbackQuery,
        callback_data: UserUpdateCallback,
        bot: Bot
    ) -> None:
        await callback_query.answer(text="🔄 Updating user data...")

        user_id = callback_data.user_id
        message = callback_query.message

        photo, caption, tg_link, full_name = await make_user_card_info(
            bot, user_id
        )

        await message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=build_user_card_keyboard(user_id, tg_link)
        )

        with suppress(TelegramBadRequest):
            await bot.edit_forum_topic(
                chat_id=forum_id,
                message_thread_id=message.message_thread_id,
                name=full_name
            )

    @router.callback_query(
        WipeForumTopicCallback.filter(F.type == "wipe")
    )
    async def handle_wipe_forum_topic(
        callback_query: CallbackQuery,
        bot: Bot,
        db: DBClient,
        forum_topic_record: dict[str, int | str]
    ) -> None:
        await callback_query.answer(text="🗑️ Wiping forum topic...")

        forum_topic_message_ids = [
            item["key"]
            for item in await db.fetch_many(
                table=messages_table,
                query=dict(user_chat_id=forum_topic_record["chat_id"])
            )
        ]

        await db.delete_many(table=messages_table, keys=forum_topic_message_ids)
        await db.delete(table=topics_table, key=forum_topic_record["key"])

        await bot.delete_forum_topic(
            chat_id=forum_id,
            message_thread_id=forum_topic_record["forum_topic_id"]
        )

    @router.message_reaction()
    async def handle_message_reaction_in_forum(
        message_reaction: MessageReactionUpdated,
        bot: Bot,
        db: DBClient,
        messages_record: dict[str, int | str]
    ) -> None:
        admin_reaction = message_reaction.new_reaction

        user_chat_id = messages_record["user_chat_id"]
        user_chat_message_id = messages_record["user_chat_message_id"]

        if premium_reactions := tuple(
            filter(lambda r: isinstance(r, ReactionTypeCustomEmoji), admin_reaction)
        ):
            if any(r.custom_emoji_id == TRASH_EMOJI_ID for r in premium_reactions):
                await bot.delete_message(chat_id=forum_id, message_id=message_reaction.message_id)
                await bot.delete_message(chat_id=user_chat_id, message_id=user_chat_message_id)
                await db.delete(table=messages_table, key=messages_record["key"])
            return

        await bot.set_message_reaction(
            chat_id=user_chat_id,
            message_id=user_chat_message_id,
            reaction=admin_reaction,
            is_big=True
        )

    return router
