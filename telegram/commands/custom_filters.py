from aiogram.dispatcher.filters import Command, Filter
from aiogram.types import Message

from ..db import db


class CommandAbout(Command):
    def __init__(self):
        super().__init__(['about'])


class CommandEmail(Command):
    def __init__(self):
        super().__init__(['email'])


class CommandGitHub(Command):
    def __init__(self):
        super().__init__(['github'])


class CommandLinkedIn(Command):
    def __init__(self):
        super().__init__(['linkedin'])


class CommandCurrentProject(Command):
    def __init__(self):
        super().__init__(['current_project'])


class CommandSignal(Command):
    def __init__(self):
        super().__init__(['signal'])


class UserModeFilter(Filter):
    async def check(self, message: Message):
        return db.get_user_mode(message.from_user.id)
