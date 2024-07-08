import asyncio
from types import TracebackType
from typing import Self

import orjson
from aiohttp import (
    BytesPayload,
    ClientSession
)


class DBClient:
    __slots__ = ("_base_url", "_base_path", "_project_key", "_session")

    def __init__(self, base_url: str, project_key: str, project_id: str):
        self._base_url = base_url
        self._base_path = f"/v1/{project_id}"
        self._project_key = project_key
        self._session = None

    @classmethod
    def from_project_key(cls, base_url: str, project_key: str) -> "DBClient":
        return cls(
            base_url=base_url,
            project_key=project_key,
            project_id=project_key.split("_")[0]
        )

    async def get_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                base_url=self._base_url,
                headers={
                    "Content-type": "application/json",
                    "X-API-Key": self._project_key
                }
            )

        return self._session

    async def fetch(self, table: str, query: dict[str, int]) -> dict[str, int] | None:
        session = await self.get_session()

        async with session.post(
            url=f"{self._base_path}/{table}/query",
            data=BytesPayload(
                value=orjson.dumps({"query": [query], "limit": 1}),
                content_type="application/json"
            )
        ) as response:
            _json = await response.json(
                encoding="utf-8",
                loads=orjson.loads
            )

            if items := _json["items"]:
                del items[0]["key"]
                return items[0]

            return

    async def put(self, table: str, data: dict[str, int]) -> dict[str, int]:
        session = await self.get_session()

        async with session.put(
            url=f"{self._base_path}/{table}/items",
            data=BytesPayload(
                value=orjson.dumps({"items": [data]}),
                content_type="application/json"
            )
        ) as response:
            items = await response.json(
                encoding="utf-8",
                loads=orjson.loads
            )

            if items := items["processed"]["items"]:
                del items[0]["key"]
                return items[0]

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
            await asyncio.sleep(0.25)
