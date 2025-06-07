from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def news_kb(current_index: int):
    buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"prev_{current_index}"),
        InlineKeyboardButton(text="⭐", callback_data=f"fav_{current_index}"),
        InlineKeyboardButton(text="➡️", callback_data=f"next_{current_index}")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard