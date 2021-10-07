from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, IDFilter
from aiogram.types import ContentTypes, Message
from aiogram.utils.markdown import escape_md, text

from .custom_commands import (
    CommandAbout,
    CommandEmail,
    CommandGitHub,
    CommandLinkedIn,
    CommandSignal,
)
from .utils import forward_to_channel, inline_reply_markup_link, user_launched_bot

from ..config import bot_admin
from ..db import db
from ..logos import Logos


FORWARD_TYPES = ContentTypes.DOCUMENT | ContentTypes.PHOTO | ContentTypes.TEXT


def register_handlers(dp: Dispatcher):
    @dp.message_handler(
        CommandStart()
    )
    async def start_handler(message: Message):
        from_user = message.from_user

        await (
            await message.answer(
                text(
                    escape_md(f"Send me your message now. "),
                    f"I will reply *as soon as I can* "
                )
            )
        ).pin()

        mention = from_user.get_mention(as_html=False)
        await user_launched_bot(dp, mention, from_user.id)

    @dp.message_handler(
        IDFilter(bot_admin),
        content_types=ContentTypes.ANY
    )
    async def reply_handler(message: Message):
        if message.reply_to_message.forward_from:
            await message.send_copy(message.reply_to_message.forward_from.id)
        else:
            message_id = message.reply_to_message.message_id - 1
            original_from_user_id = db.get_message_data(message_id)
            await message.copy_to(original_from_user_id)  #, reply_to_message_id=message_id)
        return

    @dp.message_handler(
        CommandAbout()
    )
    @forward_to_channel
    async def about_handler(message: Message):
        await message.answer(
            text(
                "*Age*: 24",
                f"*Can speak*: {escape_md('🇷🇺(native), 🇬🇧(C2), 🇩🇪(~B1)')}",
                sep="\n"
            )
        )

    @dp.message_handler(
        CommandEmail()
    )
    @forward_to_channel
    async def email_handler(message: Message):
        await message.answer_photo(
            photo=Logos.PROTONMAIL,
            caption=escape_md("wkpn@protonmail.ch")
        )

    @dp.message_handler(
        CommandGitHub()
    )
    @forward_to_channel
    async def github_handler(message: Message):
        await message.answer_photo(
            photo=Logos.GITHUB,
            reply_markup=inline_reply_markup_link(
                "GitHub", "https://github.com/wkpn"
            )
        )

    @dp.message_handler(
        CommandLinkedIn()
    )
    @forward_to_channel
    async def linkedin_handler(message: Message):
        await message.answer_photo(
            photo=Logos.LINKEDIN,
            reply_markup=inline_reply_markup_link(
                "LinkedIn", "https://www.linkedin.com/in/wkpn/"
            )
        )

    @dp.message_handler(
        CommandSignal()
    )
    @forward_to_channel
    async def signal_handler(message: Message):
        await message.answer_photo(
            photo=Logos.SIGNAL,
            reply_markup=inline_reply_markup_link(
                "+43-670-308-1866", "https://signal.org/download/"
            )
        )

    @dp.message_handler(
        content_types=FORWARD_TYPES
    )
    @forward_to_channel
    async def forward_handler(message: Message):
        forwarded_to_me = await message.forward(bot_admin)

        if not forwarded_to_me.forward_from:
            message_id = message.message_id
            from_user_id = message.from_user.id

            db.store_message_data(message_id, from_user_id)

    @dp.message_handler(
        content_types=ContentTypes.ANY
    )
    async def trash_handler(message: Message):
        await message.delete()
