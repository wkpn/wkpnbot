from datetime import datetime as dt

from aiogram import (
    F,
    Router
)
from aiogram.types import CallbackQuery

from ...utils import EditedMessageCallback


def attach_view_edited_message_edit_date_handler(router: Router) -> None:
    @router.callback_query(
        EditedMessageCallback.filter(F.type == "edited")
    )
    async def handle_view_edited_message_edit_date(
        callback_query: CallbackQuery,
        callback_data: EditedMessageCallback
    ) -> None:
        edit_date = dt.utcfromtimestamp(
            callback_data.edit_date
        ).strftime("%B %d, %Y %H:%M UTC")

        await callback_query.answer(
            text=f"This message was edited on {edit_date}",
            show_alert=True
        )
