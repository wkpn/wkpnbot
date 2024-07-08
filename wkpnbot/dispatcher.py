from typing import Any

import orjson
from aiogram import (
    Bot,
    Dispatcher
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from .routers import configure_dispatcher


def create_bot_and_dispatcher(bot_token: str, **kwargs: Any) -> tuple[Bot, Dispatcher]:
    def _orjson_dumps(value):
        return orjson.dumps(value).decode()

    bot = Bot(
        token=bot_token,
        session=AiohttpSession(
            json_loads=orjson.loads,
            json_dumps=_orjson_dumps
        ),
        default=DefaultBotProperties(
            allow_sending_without_reply=True,
            parse_mode=ParseMode.MARKDOWN_V2,
            protect_content=False
        )

    )
    dp = Dispatcher(name="dispatcher", db=kwargs.pop("db"))

    configure_dispatcher(dp, **kwargs)

    return bot, dp
