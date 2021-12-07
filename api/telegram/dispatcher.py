from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from .config import TOKEN
from .handlers import register_handlers


def bot_dispatcher() -> Dispatcher:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    dispatcher = Dispatcher(bot)

    Bot.set_current(dispatcher.bot)
    Dispatcher.set_current(dispatcher)

    register_handlers(dispatcher)

    return dispatcher


dp: Dispatcher = bot_dispatcher()
