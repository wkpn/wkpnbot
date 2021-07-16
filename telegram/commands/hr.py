from aiogram import Dispatcher
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    Message
)

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
        "HR commands are enabled",
        reply_markup=build_reply_markup(True)
    )
