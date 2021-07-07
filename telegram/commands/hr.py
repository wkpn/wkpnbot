from aiogram import Dispatcher
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    Message
)
from aiogram.utils.markdown import escape_md

from ..build_reply_markup import build_reply_markup


async def register_hr_commands(dp: Dispatcher, message: Message):
    await dp.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    await dp.bot.set_my_commands(
        [
            BotCommand(command="about", description="About"),
            BotCommand(command="current_project", description="Current project info"),
            BotCommand(command="email", description="Email"),
            BotCommand(command="github", description="GitHub"),
            BotCommand(command="linkedin", description="LinkedIn"),
            BotCommand(command="signal", description="Signal")
        ],
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    await message.answer(
        "HR commands are enabled\n\n"
        f"{escape_md('They make take some time to disappear: close the chat')} "
        f"{escape_md('and then re-open it or restart Telegram if you are')} "
        f"{escape_md('using mobile app - this is a current client behavior')}",
        reply_markup=build_reply_markup(True)
    )
