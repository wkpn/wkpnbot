from aiogram.types import Update
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK

from .security import secure_endpoint

from ..telegram import dp, SECRET


def build_webhook() -> Route:
    @secure_endpoint
    async def webhook_handler(request: Request) -> Response:
        raw_update = await request.json()
        telegram_update = Update(**raw_update)

        try:
            await dp.process_update(telegram_update)
        finally:
            return Response(status_code=HTTP_200_OK)

    webhook = Route(f"/webhook-{SECRET}", webhook_handler, methods=["POST"])

    return webhook
