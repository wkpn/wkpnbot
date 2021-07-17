from aiogram import Dispatcher
from aiogram.types import (
    BotCommandScopeChat,
    Message
)

from ..reply_markup import hr_reply_markup


async def register_user_commands(
    dp: Dispatcher, message: Message, is_start: bool = True
):
    await dp.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    if not is_start:
        await message.answer(
            "HR commands are disabled",
            reply_markup=hr_reply_markup(False)
        )
