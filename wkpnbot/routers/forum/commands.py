from aiogram import (
    F,
    Router
)
from aiogram.types import Message

from .helpers import CommandWipeForumTopic
from ...utils import build_wipe_forum_topic_keyboard


def build_forum_commands_router(forum_id: int) -> Router:
    """
    Router that handles commands in a forum topic.
    """

    router = Router(name="forum.commands")

    router.message.filter(F.chat.id == forum_id)

    @router.message(F.text, CommandWipeForumTopic())
    async def handle_wipe_forum_topic_command(
        message: Message
    ) -> None:
        await message.answer(
            text="Click on this button to wipe",
            reply_markup=build_wipe_forum_topic_keyboard()
        )

    return router
