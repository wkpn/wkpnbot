from deta import Deta

from .config import PROJECT_KEY


class DB:
    def __init__(self, project_key: str):
        self._deta = Deta(project_key)
        self._db = self._deta.Base("db")

    def set_message_data(self, message_id: int, from_user_id: int) -> None:
        self._db.put(
            data={"from_user_id": from_user_id},
            key=str(message_id)
        )

    def get_message_data(self, message_id: int) -> int:
        return self._db.get(key=str(message_id)).get("from_user_id")

    def block_user(self, user_id: int) -> None:
        self._db.put(
            data=True,
            key=str(user_id)
        )

    def unblock_user(self, user_id: int) -> None:
        self._db.put(
            data=False,
            key=str(user_id)
        )

    def is_user_blocked(self, user_id: int) -> bool:
        try:
            return self._db.get(key=str(user_id)).get("value")
        except AttributeError:
            return False


deta_db = DB(PROJECT_KEY)
