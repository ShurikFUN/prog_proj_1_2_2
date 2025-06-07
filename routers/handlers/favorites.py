from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage.fav_storage import NewsFavoritesStorage
from utils.news_format import format_news
from aiogram.filters import Command
from keyboards.delete_kb import delete_fav_kb


router = Router()
storage = NewsFavoritesStorage("storage/news_favourites.json")

#добавление в избранное
@router.callback_query(F.data.startswith("fav_"))
async def add_to_favourites(callback: CallbackQuery, state: FSMContext):
    index_str = callback.data.removeprefix("fav_")

    try:
        current_index = int(index_str)
    except ValueError:
        await callback.answer("Invalid index")
        return

    data = await state.get_data()
    news_list = data.get("news_list", [])

    if not news_list:
        await callback.answer("No news")
        return

    news_item = news_list[current_index]
    await storage.add(callback.from_user.id, news_item)
    await callback.answer("Done!")
    await callback.message.answer("News added to favourites")

#список избранного
@router.callback_query(F.data == "listfav")
async def list_favourites(callback: CallbackQuery):
    favs = await storage.list(callback.from_user.id)
    if not favs:
        return await callback.message.answer("No favourite news yet")

    kb = InlineKeyboardBuilder()
    for item in favs:
        title = item.get("title", "None")
        kb.button(text=f"Deleate: {title[:30]}", callback_data=f"newsdel_{title[:50]}")
    kb.adjust(1)

    text = "Favourite news:\n\n" + "\n\n".join(f"{format_news(n)}" for n in favs[:5])
    await callback.message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()


#удаление по кнопке
@router.callback_query(F.data.startswith("newsdel_"))
async def remove_from_favourites(callback: CallbackQuery):
    title = callback.data.removeprefix("newsdel_")

    await storage.remove(callback.from_user.id, title)
    await callback.answer("Deleted")

@router.message(Command("favourites"))
async def favourites_command(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        await message.answer("No favourite news yet")
        return

    for item in favs:
        text = format_news(item)
        keyboard=delete_fav_kb(item["article_id"])

        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")



@router.callback_query(F.data.startswith("delfav_"))
async def delete_favourite(callback: CallbackQuery):
    article_id = callback.data.removeprefix("delfav_")
    user_id = callback.from_user.id

    favs = await storage.list(user_id)
    updated_favs = [n for n in favs if n.get("article_id") != article_id]
    await storage.set(user_id, updated_favs)

    await callback.answer("Удалено из избранного")
    await callback.message.delete()
