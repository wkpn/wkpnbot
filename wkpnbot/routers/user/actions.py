from typing import NoReturn

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.types import (
    Message,
    MessageReactionUpdated,
    ReactionTypeEmoji,
    ReplyParameters
)

from ..edit_message import edit_message


def build_user_actions_router(forum_id: int) -> Router:
    """
    All subsequent user interactions take place here.
    User can send a message (can be forwarded, can be a reply, can contain media, etc.).
    User can edit an already sent message.
    User can react to any message in the chat with the bot.
    """

    router = Router(name="user.actions")

    router.edited_message.filter(F.chat.type == ChatType.PRIVATE)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.message_reaction.filter(F.chat.type == ChatType.PRIVATE)

    @router.message()
    async def handle_message_from_user(
        message: Message,
        forum_topic_record: dict[str, int],
        reply_parameters: ReplyParameters | None = None
    ) -> tuple[int, int]:
        message_thread_id = forum_topic_record["forum_topic_id"]

        if message.forward_origin:
            sent_to_topic = await message.forward(
                chat_id=forum_id,
                message_thread_id=message_thread_id
            )
        else:
            sent_to_topic = await message.copy_to(
                chat_id=forum_id,
                message_thread_id=message_thread_id,
                reply_parameters=reply_parameters
            )

        return message.message_id, sent_to_topic.message_id

    @router.edited_message()
    async def handle_edited_message_from_user(
        edited_message: Message,
        bot: Bot,
        messages_record: dict[str, int]
    ) -> NoReturn:
        forum_message_id = messages_record["forum_message_id"]

        await edit_message(
            bot=bot,
            chat_id=forum_id,
            edited_message=edited_message,
            message_id=forum_message_id
        )

    @router.message_reaction()
    async def handle_message_reaction_from_user(
        message_reaction: MessageReactionUpdated,
        bot: Bot,
        messages_record: dict[str, int]
    ) -> NoReturn:
        user_reactions = message_reaction.new_reaction

        if message_reaction.user.is_premium:
            # filter for regular reactions, this can yield more than one
            # we need to take the last one
            user_reactions = list(filter(lambda r: isinstance(r, ReactionTypeEmoji), user_reactions))[-1:]

        forum_message_id = messages_record["forum_message_id"]

        await bot.set_message_reaction(
            chat_id=forum_id,
            message_id=forum_message_id,
            reaction=user_reactions,
            is_big=True
        )

    return router
