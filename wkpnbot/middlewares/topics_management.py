from typing import Any, Awaitable, Callable

from aiogram import Bot, BaseMiddleware
from aiogram.types import Message
from cachetools import LRUCache

from ..db import DBClient
from ..utils import build_user_card_keyboard, prepare_user_card_info
from ..utils.defaults import DEFAULT_EMOJI


class TopicsManagementMiddleware(BaseMiddleware):
    """
    Middleware for managing data between users and their respective topics in the forum.
    Tries to find the topic in the cache first. If not found, tries to get the
    record from the database. In case database record is empty, creates a topic for
    the user and caches it (guaranteed to happen on a first /start command from the user).
    """

    def __init__(self, forum_id: int, table: str, cache_size: int = 10):
        self._forum_id = forum_id
        self._table = table
        self._cache = LRUCache(maxsize=cache_size)

    async def find_topic(
        self,
        db: DBClient,
        *,
        chat_id: int | None = None,
        forum_topic_id: int | None = None
    ) -> dict[str, int] | None:
        if chat_id:
            if chat_id in self._cache:
                return self._cache[chat_id]

            query = dict(chat_id=chat_id)
        else:
            for forum_topic in self._cache.values():
                if forum_topic["forum_topic_id"] == forum_topic_id:
                    return forum_topic

            query = dict(forum_topic_id=forum_topic_id)

        if forum_topic_record := await db.fetch(table=self._table, query=query):
            self._cache[forum_topic_record["chat_id"]] = forum_topic_record

            return forum_topic_record

        return

    async def create_topic(
        self,
        db: DBClient,
        *,
        bot: Bot,
        user_chat_id: int,
        message: Message
    ) -> dict[str, int]:
        user_forum_topic = await bot.create_forum_topic(
            chat_id=self._forum_id,
            name=message.from_user.full_name,
            icon_custom_emoji_id=DEFAULT_EMOJI
        )

        photo, caption, user_link, _ = await prepare_user_card_info(bot, user_chat_id)
        reply_markup = build_user_card_keyboard(user_chat_id, user_link)

        await bot.send_photo(
            chat_id=self._forum_id,
            photo=photo,
            message_thread_id=user_forum_topic.message_thread_id,
            caption=caption,
            reply_markup=reply_markup
        )

        self._cache[user_chat_id] = await db.put(
            table=self._table,
            data=dict(
                chat_id=user_chat_id,
                forum_topic_id=user_forum_topic.message_thread_id
            )
        )

        return self._cache[user_chat_id]

    async def __call__(
        self,
        handler: Callable[
            [Message, dict[str, Any]], Awaitable[Any]
        ],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        db = data["db"]
        event_context = data["event_context"]
        chat_id = event_context.chat_id

        if chat_id == self._forum_id:
            forum_topic_record = await self.find_topic(
                db, forum_topic_id=event_context.thread_id
            )
        else:
            if not (forum_topic_record := await self.find_topic(
                db, chat_id=chat_id
            )):
                forum_topic_record = await self.create_topic(
                    db, bot=data["bot"], user_chat_id=chat_id, message=event
                )

        data["forum_topic_record"] = forum_topic_record

        return await handler(event, data)
