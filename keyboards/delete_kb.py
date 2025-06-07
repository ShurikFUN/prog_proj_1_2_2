from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def delete_fav_kb(article_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Delete", callback_data=f"delfav_{article_id}")]
    ])
