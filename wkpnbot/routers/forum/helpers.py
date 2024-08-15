from aiogram.filters.command import Command


class CommandWipeForumTopic(Command):
    def __init__(self):
        super().__init__("wipe")
