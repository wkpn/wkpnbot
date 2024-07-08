from aiogram import md
from aiogram.filters.command import Command


class CommandPrivacy(Command):
    def __init__(self):
        super().__init__("privacy")


def greetings(user_first_name: str) -> str:
    name = md.bold(md.quote(user_first_name))
    return f"Hello, {name}, leave me a message 👋"
