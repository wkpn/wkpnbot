from aiogram import F, Router, md
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message


def _greetings(user_first_name: str, language_code: str) -> str:
    name = md.bold(md.quote(user_first_name))

    match language_code:
        case "de":
            return f"Hallo, {name}, hinterlassen Sie mir eine Nachricht 👋"
        case "ru":
            return f"Привет, {name}, оставь своё сообщение 👋"
        case _:
            return f"Hello, {name}, leave me a message 👋"


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
        user_first_name = message.from_user.first_name
        language_code = message.from_user.language_code
        greetings_text = _greetings(user_first_name, language_code)

        await message.answer(greetings_text)

    return router
