from aiogram import Dispatcher
from aiogram.types import ContentTypes, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import escape_md, link, text

from .app_icons.icons import Icons
from .config import channel_id, whitelist


FORWARD_TYPES = ContentTypes.TEXT | ContentTypes.PHOTO | ContentTypes.DOCUMENT


def register_commands(dp: Dispatcher):
    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["start"]
    )
    async def start_handler(message: Message):
        await message.answer(
            text(
                escape_md("Send me your message now."),
                f"I will reply *as soon as I can*"
            )
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
        commands=["about"]
    )
    async def about_handler(message: Message):
        await message.answer(
            f"Age: 24\n"
            f"{escape_md('Can speak: 🇷🇺(native), 🇬🇧(C2), 🇩🇪(~B1)')}\n"
            f"Main skill: Python\n"
            f"{escape_md('Prod. experience: 4+ y.')}\n"
            f"Working at: EPAM Systems\n"
            f"Title: Software Engineer\n"
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["email"]
    )
    async def email_handler(message: Message):
        await message.answer_photo(
            photo=Icons.PROTONMAIL,
            caption=escape_md("wkpn@protonmail.ch")
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["github"]
    )
    async def github_handler(message: Message):
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(
            text="GitHub", url="https://github.com/wkpn")
        )

        await message.answer_photo(
            photo=Icons.GITHUB,
            reply_markup=reply_markup
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["linkedin"]
    )
    async def linkedin_handler(message: Message):
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(
            text="LinkedIn", url="https://www.linkedin.com/in/whyapostrophe/")
        )

        await message.answer_photo(
            photo=Icons.LINKEDIN,
            reply_markup=reply_markup
        )

    @dp.message_handler(
        lambda msg: msg.from_user.id not in whitelist,
        commands=["current_project"]
    )
    async def current_project_handler(message: Message):
        await message.answer(
            f"Name: Distribution at Thomson Reuters\n"
            f"{escape_md('Description: Platform modernization & migration to AWS')}\n"
            f"Role: Backend Developer\n\n"
            f"{escape_md('Stack: python3.8, pytest, docker, AWS')}\n"
            f"Cloud stack: API Gateway, CloudFormation, "
            f"CloudWatch, CodeBuild, CodePipeline, DynamoDB, Lambda, SNS, SQS"
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
