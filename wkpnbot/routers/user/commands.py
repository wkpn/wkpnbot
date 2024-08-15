from aiogram import (
    F,
    Router
)
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from .helpers import (
    CommandPrivacy,
    greetings
)
from ...utils import build_privacy_policy_keyboard


def build_user_commands_router() -> Router:
    """
    Main entry point, this is where user starts the bot. Before that happens,
    forum topic is created for the user that started the bot.
    """

    router = Router(name="user.commands")

    router.message.filter(F.chat.type == ChatType.PRIVATE)

    @router.message(F.text, CommandStart())
    async def handle_start_command_from_user(
        message: Message
    ) -> None:
        greetings_text = greetings(message.from_user.first_name)

        await message.answer(text=greetings_text)

    @router.message(F.text, CommandPrivacy())
    async def handle_privacy_command_from_user(
        message: Message
    ) -> None:
        await message.answer(
            text="Click on this link to read",
            reply_markup=build_privacy_policy_keyboard()
        )

    return router
