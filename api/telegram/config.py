from starlette.config import Config


config = Config()

# database
PROJECT_KEY: str = config("PROJECT_KEY")

# telegram
BOT_ADMIN: int = config("ADMIN", cast=int)
CHANNEL_ID: int = config("CHANNEL_ID", cast=int)
TOKEN: str = config("TOKEN")

# webhook
SECRET: str = config("SECRET")
