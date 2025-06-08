from aiogram.filters import BaseFilter
from aiogram.types import Message

class NotCommandFilter(BaseFilter):
    async def __call__(self, message: Message):
        return message.text is not None and not message.text.startswith('/')
