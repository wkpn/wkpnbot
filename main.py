from aiogram.types import Update

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK

from security import check_ip
from telegram import dispatcher as dp, secret


def build_application() -> Starlette:
    async def telegram_webhook(request: Request) -> Response:
        check_ip(request.headers.get("x-real-ip"))

        raw_update = await request.json()
        telegram_update = Update(**raw_update)
        await dp.process_update(telegram_update)

        return Response(status_code=HTTP_200_OK)

    routes = [
        Route(f"/webhook-{secret}", telegram_webhook, methods=["POST"]),
    ]

    app = Starlette(routes=routes)

    return app


app = build_application()
