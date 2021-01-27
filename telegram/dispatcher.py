from aiogram import Bot, Dispatcher
from aiogram.types import ContentTypes, Message
from aiogram.utils.markdown import escape_md, text

from config import channel_id, token, whitelist


def bot_dispatcher() -> Dispatcher:
    bot = Bot(token=token, parse_mode="MarkdownV2")
    dp = Dispatcher(bot)

    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["start"]
    )
    async def start_handler(message: Message):
        await message.answer(
            text(escape_md("Send me your message now."), f"I will reply *as soon as I can*")
        )

        mention = message.from_user.get_mention(as_html=False)
        await dp.bot.send_message(
            channel_id,
            text(f"Launched by {mention}", escape_md(f"(id={message.from_user.id})"))
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
