from typing import Any, NoReturn

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

    user_actions_router = build_user_actions_router(
        forum_id=forum_id
    )
    user_actions_router.message.middleware(messages_middleware)

    admin_actions_router = build_forum_actions_router(
        forum_id=forum_id
    )
    admin_actions_router.message.middleware(messages_middleware)

    dp.include_routers(
        build_user_commands_router(),
        user_actions_router,
        admin_actions_router
    )

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION)
    )
    async def bot_added_to_chanel(
        my_chat_member: ChatMemberUpdated, bot: Bot
    ) -> NoReturn:
        """
        If somebody added this bot as a channel admin, leave the channel immediately.
        """

        await bot.leave_chat(chat_id=my_chat_member.chat.id)

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=KICKED)
    )
    async def user_blocked_bot(
        my_chat_member: ChatMemberUpdated, bot: Bot, db: DBClient
    ) -> NoReturn:
        """
        Closes the forum topic if user has blocked the bot.
        """

        record = await db.fetch(
            table=topics_table,
            query=dict(chat_id=my_chat_member.chat.id)
        )
        forum_topic_id = record["forum_topic_id"]

        await bot.close_forum_topic(chat_id=forum_id, message_thread_id=forum_topic_id)

    @dp.my_chat_member(
        ChatMemberUpdatedFilter(member_status_changed=MEMBER)
    )
    async def user_unblocked_bot(
        my_chat_member: ChatMemberUpdated, bot: Bot, db: DBClient
    ) -> NoReturn:
        """
        Reopens the forum topic if user has unblocked the bot.
        """

        record = await db.fetch(
            table=topics_table,
            query=dict(chat_id=my_chat_member.chat.id)
        )
        forum_topic_id = record["forum_topic_id"]

        await bot.reopen_forum_topic(chat_id=forum_id, message_thread_id=forum_topic_id)

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
    ) -> NoReturn:
        """
        Deletes the message that has caused an exception.
        """

        await message.delete()
