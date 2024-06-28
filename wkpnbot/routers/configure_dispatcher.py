from typing import Any

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError
)
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    ExceptionTypeFilter,
    KICKED,
    MEMBER,
    PROMOTED_TRANSITION
)
from aiogram.types import (
    ChatMemberUpdated,
    ErrorEvent,
    Message
)

from .forum import build_forum_actions_router
from .user import (
    build_user_actions_router,
    build_user_commands_router
)
from ..db import DBClient
from ..middlewares import (
    InteractionsMiddleware,
    MessagesMiddleware,
    FilterMiddleware,
    TopicsManagementMiddleware
)


def configure_dispatcher(dp: Dispatcher, **kwargs: Any) -> None:
    forum_id = kwargs["forum_id"]
    messages_table = kwargs["messages_table"]
    topics_table = kwargs["topics_table"]

    dp.message.outer_middleware(FilterMiddleware())
    dp.message.outer_middleware(
        TopicsManagementMiddleware(forum_id=forum_id, table=topics_table)
    )

    interactions_middleware = InteractionsMiddleware(
        forum_id=forum_id, table=messages_table
    )

    dp.edited_message.outer_middleware(interactions_middleware)
    dp.message_reaction.outer_middleware(interactions_middleware)

    messages_middleware = MessagesMiddleware(
        forum_id=forum_id, table=messages_table
    )

    user_commands_router = build_user_commands_router()
    user_actions_router = build_user_actions_router(
        forum_id=forum_id
    )
    user_actions_router.message.middleware(messages_middleware)

    forum_actions_router = build_forum_actions_router(
        forum_id=forum_id
    )
    forum_actions_router.message.middleware(messages_middleware)

    dp.include_routers(
        user_commands_router,
        user_actions_router,
        forum_actions_router
    )

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION)
    )
    async def bot_added_to_chanel(
        my_chat_member: ChatMemberUpdated, bot: Bot
    ) -> None:
        """
        If somebody added this bot as a channel admin, leave the channel immediately.
        """

        await bot.leave_chat(chat_id=my_chat_member.chat.id)

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=KICKED)
    )
    async def user_blocked_bot(
        my_chat_member: ChatMemberUpdated, bot: Bot, db: DBClient
    ) -> None:
        """
        Closes the forum topic if user has blocked the bot.
        """

        record = await db.fetch(
            table=topics_table,
            query=dict(chat_id=my_chat_member.chat.id)
        )

        # If the user just blocked the bot without any interactions
        # with it, there is no need to close the forum topic that
        # doesn't exist yet.

        if record:
            await bot.close_forum_topic(
                chat_id=forum_id,
                message_thread_id=record["forum_topic_id"]
            )

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=MEMBER)
    )
    async def user_unblocked_bot(
        my_chat_member: ChatMemberUpdated, bot: Bot, db: DBClient
    ) -> None:
        """
        Reopens the forum topic if user has unblocked the bot.
        """

        record = await db.fetch(
            table=topics_table,
            query=dict(chat_id=my_chat_member.chat.id)
        )

        # Check if user unblocked the bot without starting it previously.
        # In this case `my_chat_member` update will be before `message`,
        # and if there is no record for the forum topic, we don't need to
        # reopen it since it doesn't exist yet.

        if record:
            await bot.reopen_forum_topic(
                chat_id=forum_id,
                message_thread_id=record["forum_topic_id"]
            )

    @dp.error(
        ExceptionTypeFilter(
            TelegramBadRequest,
            TelegramForbiddenError,
            TelegramNetworkError
        ),
        F.update.message.as_("message")
    )
    async def handle_telegram_errors(
        exception: ErrorEvent, message: Message
    ) -> None:
        """
        Deletes the message that has caused an exception.
        """

        await message.delete()
