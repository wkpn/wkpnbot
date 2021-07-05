from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from .config import token
from .commands import register_commands


def bot_dispatcher() -> Dispatcher:
    bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher(bot)

    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)

    register_commands(dp)

    return dp


dispatcher: Dispatcher = bot_dispatcher()
