from aiogram import Router
from aiogram.types import Message
from filters.command import NotCommandFilter

router = Router()

@router.message(NotCommandFilter())
async def fallback_handler(message: Message):
    await message.answer("Sorry, i cant help you here. Try /help to find commands")