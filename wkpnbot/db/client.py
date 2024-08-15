import asyncio
import sys
from types import TracebackType

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

import orjson
from aiohttp import (
    BytesPayload,
    ClientSession
)


class DBClient:
    __slots__ = ("_base_url", "_base_path", "_data_key", "_session")

    def __init__(self, base_url: str, data_key: str, collection_id: str):
        self._base_url = base_url
        self._base_path = f"/v1/{collection_id}"
        self._data_key = data_key
        self._session = None

    @classmethod
    def from_data_key(cls, base_url: str, data_key: str) -> Self:
        return cls(
            base_url=base_url,
            data_key=data_key,
            collection_id=data_key.split("_")[0]
        )

    async def get_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                base_url=self._base_url,
                headers={
                    "Content-type": "application/json",
                    "X-API-Key": self._data_key
                }
            )

        return self._session

    async def delete(
        self, table: str, key: int | str
    ) -> None:
        session = await self.get_session()

        async with session.delete(
            url=f"{self._base_path}/{table}/items/{key}"
        ):
            # we don't care about response there
            return

    async def delete_many(
        self, table: str, keys: list[int | str]
    ) -> None:
        if not keys:
            return

        tasks = (self.delete(table=table, key=key) for key in keys)
        await asyncio.gather(*tasks)

    async def fetch(
        self, table: str, query: dict[str, int]
    ) -> dict[str, int | str] | None:
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
                return items[0]

            return

    async def fetch_many(
        self, table: str, query: dict[str, int], limit: int = 100
    ) -> list[dict[str, int | str]] | None:
        session = await self.get_session()

        items = []
        last = ""

        while True:
            async with session.post(
                url=f"{self._base_path}/{table}/query",
                data=BytesPayload(
                    value=orjson.dumps(
                        {"query": [query], "limit": limit, "last": last}
                    ),
                    content_type="application/json"
                )
            ) as response:
                _json = await response.json(
                    encoding="utf-8", loads=orjson.loads
                )

                items.extend(_json["items"])

                if _last := _json["paging"].get("last"):
                    last = _last
                else:
                    break

        if items:
            return items

        return

    async def put(
        self, table: str, item: dict[str, int]
    ) -> dict[str, int | str]:
        session = await self.get_session()

        async with session.put(
            url=f"{self._base_path}/{table}/items",
            data=BytesPayload(
                value=orjson.dumps({"items": [item]}),
                content_type="application/json"
            )
        ) as response:
            items = await response.json(
                encoding="utf-8", loads=orjson.loads
            )

            return items["processed"]["items"][0]

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
