from aiogram import Dispatcher
from aiogram.types import (
    BotCommandScopeChat,
    Message
)

from ..build_reply_markup import build_reply_markup


async def register_user_commands(
    dp: Dispatcher, message: Message, is_start: bool = True
):
    await dp.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    if not is_start:
        await message.answer(
            "HR commands are disabled",
            reply_markup=build_reply_markup(False)
        )
