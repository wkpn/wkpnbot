from starlette.config import Config


config = Config()

bot_admin: int = config("ADMIN", cast=int)
channel_id: int = config("CHANNEL_ID", cast=int)
project_key: str = config("PROJECT_KEY")
secret: str = config("SECRET")
token: str = config("TOKEN")
