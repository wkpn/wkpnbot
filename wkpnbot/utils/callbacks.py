from aiogram.filters.callback_data import CallbackData


class UserUpdateCallback(CallbackData, prefix="user"):
    type: str
    user_id: int
    random_data: str
