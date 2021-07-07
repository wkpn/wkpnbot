from aiogram import Dispatcher
from aiogram.types import (
    ContentTypes,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.markdown import escape_md, text

from .hr import register_hr_commands
from .user import register_user_commands

from ..build_reply_markup import build_reply_markup
from ..db import DB
from ..config import channel_id, whitelist
from ..logos import Icons


FORWARD_TYPES = ContentTypes.TEXT | ContentTypes.PHOTO | ContentTypes.DOCUMENT


def register_commands(dp: Dispatcher):
    db = DB()

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["start"]
    )
    async def start_handler(message: Message):
        db.update_user_mode(False, user_id=message.from_user.id)
        await register_user_commands(dp, message)

        reply_keyboard_markup = build_reply_markup(False)

        await message.answer(
            text(
                escape_md(f"Send me your message now. "),
                f"I will reply *as soon as I can* "
            ),
            reply_markup=reply_keyboard_markup
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
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: not db.get_user_mode(msg.from_user.id),
        lambda msg: msg.text == "I'm HR",
    )
    async def switch_to_hr_mode(message: Message):
        db.update_user_mode(True, user_id=message.from_user.id)

        await register_hr_commands(dp, message)
        return

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        lambda msg: msg.text == "I'm not HR",
    )
    async def switch_to_user_mode(message: Message):
        db.update_user_mode(False, user_id=message.from_user.id)

        await register_user_commands(dp, message, False)
        return

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        commands=["about"]
    )
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
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        commands=["email"]
    )
    async def email_handler(message: Message):
        await message.answer_photo(
            photo=Icons.PROTONMAIL,
            caption=escape_md("wkpn@protonmail.ch")
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        commands=["github"]
    )
    async def github_handler(message: Message):
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(
            InlineKeyboardButton(
                text="GitHub", url="https://github.com/wkpn"
            )
        )

        await message.answer_photo(
            photo=Icons.GITHUB,
            reply_markup=reply_markup
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        commands=["linkedin"]
    )
    async def linkedin_handler(message: Message):
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(
            InlineKeyboardButton(
                text="LinkedIn", url="https://www.linkedin.com/in/wkpn/"
            )
        )

        await message.answer_photo(
            photo=Icons.LINKEDIN,
            reply_markup=reply_markup
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        lambda msg: db.get_user_mode(msg.from_user.id),
        commands=["current_project"]
    )
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
        lambda msg: msg.from_user.id not in whitelist,
        commands=["signal"]
    )
    async def signal_handler(message: Message):
        await message.answer_photo(
            photo=Icons.SIGNAL,
            caption=escape_md("+1-562-352-0058")
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        content_types=FORWARD_TYPES
    )
    async def forward_handler(message: Message):
        await message.forward(channel_id)

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        content_types=ContentTypes.ANY
    )
    async def trash_handler(message: Message):
        await message.delete()
