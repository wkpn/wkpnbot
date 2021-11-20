from deta import Deta

from .config import project_key


class DB:
    def __init__(self, project_key: str):
        self._deta = Deta(project_key)
        self._db = self._deta.Base("db")

    def set_message_data(self, message_id: int, from_user_id: int):
        self._db.put(
            data={"from_user_id": from_user_id},
            key=str(message_id)
        )

    def get_message_data(self, message_id: str):
        return self._db.get(key=str(message_id)).get("from_user_id")


db = DB(project_key)
