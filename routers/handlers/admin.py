from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram import Bot

router = Router()

#функция для проверки прав админа
@router.message(Command("admin"))
async def admin_panel_handler(message: Message):
    try:
        await message.answer("""
        Welcome aboard, captain, all systems online
        /stats
        """)
    except Exception as e:
        print(f"Error sending message: {e}")

@router.message(Command("stats"))
async def stats_handler(message: Message, state: FSMContext):
    storage = state.storage
    user_count = await storage.get_user_count()
    await message.answer(f"Amount of users in bd: {user_count}")
