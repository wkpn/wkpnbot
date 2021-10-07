from aiogram.dispatcher.filters import Command


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


class CommandSignal(Command):
    def __init__(self):
        super().__init__(['signal'])
