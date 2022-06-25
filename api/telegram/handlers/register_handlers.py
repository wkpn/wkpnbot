from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, IDFilter
from aiogram.types import ContentTypes, Message
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import text

from .utils import (
    forward_to_channel,
    user_launched_bot,
    user_not_blocked
)

from ..config import BOT_ADMIN
from ..db import deta_db


FORWARD_TYPES = ContentTypes.DOCUMENT | ContentTypes.PHOTO | ContentTypes.TEXT


def register_handlers(dp: Dispatcher):
    @dp.message_handler(
        CommandStart()
    )
    @user_launched_bot
    @user_not_blocked
    async def start_handler(message: Message):
        await (
            await message.answer(
                text(
                    f"Send me your message now, I will reply *as soon as I can*",
                    f"I am *not looking for job offers* at this moment",
                    sep="\n"
                )
            )
        ).pin()

    @dp.message_handler(
        IDFilter(BOT_ADMIN),
        content_types=ContentTypes.ANY
    )
    async def reply_handler(message: Message):
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
        else:
            message_id = message.reply_to_message.message_id - 1
            user_id = deta_db.get_message_data(message_id)
        try:
            if message.text == "!block":
                deta_db.block_user(user_id)
                await message.reply(f"User {user_id} is blocked now")
                await dp.bot.send_message(user_id, "You were blocked")
            elif message.text == "!unblock":
                deta_db.unblock_user(user_id)
                await message.reply(f"User {user_id} is unblocked now")
                await dp.bot.send_message(user_id, "You were unblocked")
            else:
                await message.send_copy(user_id)
        except BotBlocked:
            await message.reply("User has blocked the bot")
        finally:
            return

    @dp.message_handler(
        content_types=FORWARD_TYPES
    )
    @user_not_blocked
    @forward_to_channel
    async def forward_handler(message: Message):
        forwarded_to_me = await message.forward(BOT_ADMIN)

        if not forwarded_to_me.forward_from:
            message_id = message.message_id
            from_user_id = message.from_user.id

            deta_db.set_message_data(message_id, from_user_id)

    @dp.message_handler(
        content_types=ContentTypes.ANY
    )
    async def trash_handler(message: Message):
        await message.delete()
