
from aiogram import BaseMiddleware
from aiogram.types import Message
from config.settings_admin import admin_config

admins = {int(admin_config.telegram_key)}

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        print("admin")
        if event.text and event.text == '/adminpanel':
            if user_id not in admins:
                await event.answer("Access is denied")
                return
        return await handler(event, data)
