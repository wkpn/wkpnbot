from aiogram import Bot, Dispatcher
from aiogram.types import (
    ContentTypes,
    Message
)

from config import channel_id, token, whitelist


def bot_dispatcher() -> Dispatcher:
    bot = Bot(token=token)
    dp = Dispatcher(bot)

    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["start"]
    )
    async def start_handler(message: Message):
        await message.reply("I will reply as soon as I can")

        mention = message.from_user.get_mention(as_html=True)
        await dp.bot.send_message(
            channel_id, f"Launched by {mention} (id={message.from_user.id})", parse_mode="HTML"
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        content_types=ContentTypes.TEXT | ContentTypes.PHOTO | ContentTypes.DOCUMENT
    )
    async def forward_handler(message: Message):
        await message.forward(channel_id)

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        content_types=ContentTypes.ANY
    )
    async def trash_handler(message: Message):
        await message.delete()

    return dp


dispatcher: Dispatcher = bot_dispatcher()
