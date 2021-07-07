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
