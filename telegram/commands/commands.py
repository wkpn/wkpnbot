from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, IDFilter, Text
from aiogram.types import ContentTypes, Message
from aiogram.utils.markdown import escape_md, text

from .custom_filters import (
    CommandAbout,
    CommandCurrentProject,
    CommandEmail,
    CommandGitHub,
    CommandLinkedIn,
    CommandSignal,
    UserModeFilter
)
from .hr import register_hr_commands
from .user import register_user_commands

from ..config import bot_admin, channel_id
from ..db import db
from ..logos import Icons
from ..reply_markup import hr_reply_markup, inline_reply_markup_link


FORWARD_TYPES = ContentTypes.TEXT | ContentTypes.PHOTO | ContentTypes.DOCUMENT


def forward_to_channel(func):
    async def wrapped(message: Message):
        result = await func(message)
        await message.forward(channel_id, disable_notification=True)
        return result
    return wrapped


def register_commands(dp: Dispatcher):
    @dp.message_handler(
        CommandStart()
    )
    async def start_handler(message: Message):
        db.update_user_mode(False, user_id=message.from_user.id)
        await register_user_commands(dp, message)

        await message.answer(
            text(
                escape_md(f"Send me your message now. "),
                f"I will reply *as soon as I can* "
            ),
            reply_markup=hr_reply_markup(False)
        )

        mention = message.from_user.get_mention(as_html=False)
        await dp.bot.send_message(
            channel_id,
            text(
                f"Launched by {mention}",
                escape_md(f"(id={message.from_user.id})")
            )
        )

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
        ~UserModeFilter(),
        Text("I'm HR"),
    )
    async def switch_to_hr_mode(message: Message):
        db.update_user_mode(True, user_id=message.from_user.id)

        await register_hr_commands(dp, message)
        return

    @dp.message_handler(
        UserModeFilter(),
        Text("I'm not HR"),
    )
    async def switch_to_user_mode(message: Message):
        db.update_user_mode(False, user_id=message.from_user.id)

        await register_user_commands(dp, message, False)
        return

    @dp.message_handler(
        UserModeFilter(),
        CommandAbout()
    )
    @forward_to_channel
    async def about_handler(message: Message):
        await message.answer(
            text(
                "*Age*: 24",
                f"*Can speak*: {escape_md('🇷🇺(native), 🇬🇧(C2), 🇩🇪(~B1)')}",
                "*Main skill*: Python",
                f"*Production experience*: {escape_md('4+ y.')}",
                "*Working at*: EPAM Systems",
                "*Title*: Software Engineer",
                sep="\n"
            )
        )

    @dp.message_handler(
        UserModeFilter(),
        CommandEmail()
    )
    @forward_to_channel
    async def email_handler(message: Message):
        await message.answer_photo(
            photo=Icons.PROTONMAIL,
            caption=escape_md("wkpn@protonmail.ch")
        )

    @dp.message_handler(
        UserModeFilter(),
        CommandGitHub()
    )
    @forward_to_channel
    async def github_handler(message: Message):
        await message.answer_photo(
            photo=Icons.GITHUB,
            reply_markup=inline_reply_markup_link(
                "GitHub", "https://github.com/wkpn"
            )
        )

    @dp.message_handler(
        UserModeFilter(),
        CommandLinkedIn()
    )
    @forward_to_channel
    async def linkedin_handler(message: Message):
        await message.answer_photo(
            photo=Icons.LINKEDIN,
            reply_markup=inline_reply_markup_link(
                "LinkedIn", "https://www.linkedin.com/in/wkpn/"
            )
        )

    @dp.message_handler(
        UserModeFilter(),
        CommandCurrentProject()
    )
    @forward_to_channel
    async def current_project_handler(message: Message):
        await message.answer(
            text(
                "*Name*: Distribution at Thomson Reuters",
                f"*Description*: {escape_md('Platform modernization & migration to AWS')}",
                "*Role*: Backend Developer",
                f"*Stack*: {escape_md('python3.8, pytest, docker, AWS')}",
                "*Cloud stack*: API Gateway, CloudFormation, "
                "CloudWatch, CodeBuild, CodePipeline, DynamoDB, Lambda, SNS, SQS",
                sep="\n"
            )
        )

    @dp.message_handler(
        UserModeFilter(),
        CommandSignal()
    )
    @forward_to_channel
    async def signal_handler(message: Message):
        await message.answer_photo(
            photo=Icons.SIGNAL,
            caption=escape_md("+1-562-352-0058")
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
