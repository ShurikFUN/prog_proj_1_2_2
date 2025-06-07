from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hi! Im news bot  :)\n"
                         "Print /help to check my commands")

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def start_command(message: Message):
    await message.answer(
        "Commands:\n"
        "/topic - choose your topic\n"
        "/latest - latest news \n"
        "/favourites - check your favourites\n"
    )