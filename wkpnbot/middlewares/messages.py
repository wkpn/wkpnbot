from typing import (
    Any,
    Awaitable,
    Callable
)

from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    ReplyParameters,
    TextQuote
)


def _prepare_quote_params(quote: TextQuote | None) -> dict[str, Any]:
    if quote:
        return dict(
            quote=quote.text,
            quote_entities=quote.entities,
            quote_position=quote.position
        )
    else:
        return dict(quote=None, quote_entities=None, quote_position=None)


class MessagesMiddleware(BaseMiddleware):
    """
    Middleware for storing message pairs (user_chat_message_id - forum_message_id).
    Passes down "reply_parameters" down to handler when message is a reply.
    Writes a db record (user_chat_message_id - forum_message_id) when message is sent.
    """

    def __init__(self, forum_id: int, table: str):
        self._forum_id = forum_id
        self._table = table

    async def __call__(
        self,
        handler: Callable[
            [Message, dict[str, Any]], Awaitable[Any]
        ],
        event: Message,
        data: dict[str, Any]
    ) -> None:
        db = data["db"]
        event_context = data["event_context"]
        chat_id = event_context.chat_id
        forum_topic_record = data["forum_topic_record"]

        reply_parameters = None

        if chat_id == self._forum_id:
            # https://github.com/tdlib/telegram-bot-api/issues/356#issuecomment-1405378400
            if not event.reply_to_message.forum_topic_created:
                if record := await db.fetch(
                    table=self._table,
                    query=dict(forum_message_id=event.reply_to_message.message_id)
                ):
                    reply_parameters = ReplyParameters(
                        message_id=record["user_chat_message_id"],
                        quote_parse_mode=None,
                        **_prepare_quote_params(event.quote)
                    )
        else:
            if event.reply_to_message:
                if record := await db.fetch(
                    table=self._table,
                    query=dict(
                        user_chat_id=chat_id,
                        user_chat_message_id=event.reply_to_message.message_id
                    )
                ):
                    reply_parameters = ReplyParameters(
                        message_id=record["forum_message_id"],
                        quote_parse_mode=None,
                        **_prepare_quote_params(event.quote)
                    )

        data["reply_parameters"] = reply_parameters

        user_chat_message_id, forum_message_id = await handler(event, data)

        await db.put(
            table=self._table,
            item=dict(
                user_chat_id=forum_topic_record["chat_id"],
                user_chat_message_id=user_chat_message_id,
                forum_message_id=forum_message_id
            )
        )
