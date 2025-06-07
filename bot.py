from config.settings_bot import bot_config
from aiogram import Bot, Dispatcher
from storage.sqlite_storage import SQLiteStorage  # редис не хотел ставиться
from routers import commands
from routers.handlers import favorites, latest, topic, admin, fallback
import logging
from middleware.middleware import AdminCheckMiddleware



#логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#хэндлер (консоль)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# хэндлер (файл)
file_handler = logging.FileHandler("log", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

async def main():
    bot = Bot(token=bot_config.telegram_key)

    storage = SQLiteStorage("storage/fsm_data.db")
    dp = Dispatcher(storage=storage)

    dp.message.middleware(AdminCheckMiddleware())

    """
    TODO: прикрутить роутеры
    """

    # регистрация роутеров
    dp.include_router(admin.router)
    dp.include_router(commands.router)
    dp.include_router(latest.router)
    dp.include_router(favorites.router)
    dp.include_router(topic.router)
    dp.include_router(fallback.router)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())