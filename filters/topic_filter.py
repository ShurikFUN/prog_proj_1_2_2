from aiogram.filters import BaseFilter
from aiogram.types import Message

class TopicFilter(BaseFilter):
    valid_topics = {
        "technology", "business", "sports", "health", "politics",
        "entertainment", "science", "world", "environment"
    }

#gпроверка что сообщение текстовое и не команда
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        text = message.text.lower()
        if text.startswith('/'):
            return False
        return text in self.valid_topics
