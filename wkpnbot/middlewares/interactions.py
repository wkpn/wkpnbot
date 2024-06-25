from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, MessageReactionUpdated


class InteractionsMiddleware(BaseMiddleware):
    """
    Middleware for obtaining message pairs (user_chat_message_id - forum_message_id)
    for "edited_message" and "message_reaction" updates.
    Passes "messages_record" down to handler in the "data" field.
    """

    def __init__(self, forum_id: int, table: str):
        self._forum_id = forum_id
        self._table = table

    async def __call__(
        self,
        handler: Callable[
            [Message, dict[str, Any]], Awaitable[Any]
        ],
        event: Message | MessageReactionUpdated,
        data: dict[str, Any]
    ) -> Any:
        db = data["db"]
        event_context = data["event_context"]
        chat_id = event_context.chat_id

        if chat_id == self._forum_id:
            query = dict(forum_message_id=event.message_id)
        else:
            query = dict(
                user_chat_id=chat_id,
                user_chat_message_id=event.message_id
            )

        data["messages_record"] = await db.fetch(
            table=self._table, query=query
        )

        return await handler(event, data)
