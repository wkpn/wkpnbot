from typing import (
    Any,
    Awaitable,
    Callable
)

from aiogram import BaseMiddleware
from aiogram.enums import ContentType
from aiogram.types import Message


class FilterMiddleware(BaseMiddleware):
    """
    Middleware for handling only messages of supported "content_type".
    """

    async def __call__(
        self,
        handler: Callable[
            [Message, dict[str, Any]], Awaitable[Any]
        ],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        # those are not content types, but they are not supported anyway
        if event.external_reply or event.media_group_id:
            await event.delete()
            return

        # those are, and they can be matched
        match event.content_type:
            case (
                ContentType.FORUM_TOPIC_CLOSED |
                ContentType.FORUM_TOPIC_CREATED |
                ContentType.FORUM_TOPIC_REOPENED
            ):
                return
            case (
                ContentType.CHAT_BACKGROUND_SET |
                ContentType.DELETE_CHAT_PHOTO |
                ContentType.FORUM_TOPIC_EDITED |
                ContentType.GENERAL_FORUM_TOPIC_HIDDEN |
                ContentType.GENERAL_FORUM_TOPIC_UNHIDDEN |
                ContentType.NEW_CHAT_PHOTO |
                ContentType.NEW_CHAT_TITLE |
                ContentType.PINNED_MESSAGE |
                ContentType.POLL
            ):
                await event.delete()
                return
            # case _:
            #     await event.delete()
            #     return

        return await handler(event, data)
