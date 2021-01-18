from starlette.config import Config
from typing import List


config = Config()

channel_id: int = config("CHANNEL_ID", cast=int)
token: str = config("TOKEN")
whitelist: List[int] = list(map(int, config("WHITELIST").split(",")))
