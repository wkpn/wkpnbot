from aiogram import Dispatcher
from aiogram.types import (
    BotCommandScopeChat,
    Message
)
from aiogram.utils.markdown import escape_md

from ..build_reply_markup import build_reply_markup


async def register_user_commands(
    dp: Dispatcher, message: Message, is_start: bool = True
):
    await dp.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    if not is_start:
        await message.answer(
            "HR commands are disabled\n\n"
            f"{escape_md('They make take some time to disappear: close the chat')} "
            f"{escape_md('and then re-open it or restart Telegram if you are')} "
            f"{escape_md('using mobile app - this is a current client behavior')}",
            reply_markup=build_reply_markup(False)
        )
