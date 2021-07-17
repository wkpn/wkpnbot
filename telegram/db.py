from deta import Deta

from .config import project_key


class DB:
    def __init__(self):
        self._deta = Deta(project_key)
        self._db = self._deta.Base("db")

    def update_user_mode(self, mode: bool, user_id: str):
        self._db.put(data=mode, key=str(user_id))

    def get_user_mode(self, user_id: str):
        return self._db.get(key=str(user_id)).get("value")

    def get_reply_mode(self):
        return self._db.get(key="reply_mode").get("value")

    def store_reply_mode(self, mode: bool):
        return self._db.put(data=mode, key="reply_mode")

    def store_message_data(self, message_id: int, from_user_id: int):
        self._db.put(
            data={"from_user_id": from_user_id},
            key=str(message_id)
        )

    def get_message_data(self, message_id: str):
        return self._db.get(key=str(message_id)).get("from_user_id")


db = DB()
