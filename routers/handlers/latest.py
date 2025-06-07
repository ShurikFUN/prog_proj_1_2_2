from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.news_client import get_news
from aiogram.fsm.context import FSMContext
from keyboards.latest_kb import news_kb
from utils.news_format import format_news

router = Router()

#обработчик latest
@router.message(Command("latest"))
async def latest_handler(message: Message, state: FSMContext):
    #получаем выбранный топик из состояния
    user_data = await state.get_data()
    topic = user_data.get("topic")
    if not topic:
        await message.answer("Please choose a topic first using /topic")
        return

    #получаем новости
    news_list = await get_news(topic=topic)

    if not news_list:
        await message.answer("No news found for this topic")
        return

    #cохраняем список новостей и индекс
    await state.update_data(news_list=news_list, current_index=0)

    #форматируем первую новость и отправляем с кнопками
    first_news = news_list[0]
    text = format_news(first_news)
    keyboard = news_kb(current_index=0)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

#обработчик нажатий
@router.callback_query(F.data.startswith(("prev_", "next_")))
async def navigation_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    news_list = data.get("news_list", [])

    if not news_list:
        await callback.answer("No news available.")
        return

    action, idx_str = callback.data.split('_')
    current_index = int(idx_str)

    if action == "next":
        current_index = min(current_index + 1, len(news_list) - 1)
    elif action == "prev":
        current_index = max(current_index - 1, 0)

    await state.update_data(current_index=current_index)

    news = news_list[current_index]
    text = format_news(news)
    keyboard = news_kb(current_index)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()



