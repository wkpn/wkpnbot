from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from .handlers import register_handlers
from .config import token


def bot_dispatcher() -> Dispatcher:
    bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher(bot)

    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)

    register_handlers(dp)

    return dp


dispatcher: Dispatcher = bot_dispatcher()
