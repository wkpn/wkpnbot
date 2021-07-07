from starlette.config import Config
from typing import List


config = Config()

channel_id: int = config("CHANNEL_ID", cast=int)
project_key: str = config("PROJECT_KEY")
token: str = config("TOKEN")
secret: str = config("SECRET")
whitelist: List[int] = list(map(int, config("WHITELIST").split(",")))
