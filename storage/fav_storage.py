import json
import os
from typing import List


#создание бд для fav
class NewsFavoritesStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump({}, f)

    async def _load(self) -> dict:
        with open(self.filepath, "r") as f:
            return json.load(f)

    async def _save(self, data: dict):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    async def add(self, user_id: int, news_item: dict):
        data = await self._load()
        uid = str(user_id)
        data.setdefault(uid, [])
        if news_item not in data[uid]:
            data[uid].append(news_item)
            await self._save(data)

    async def remove(self, user_id: int, title: str):
        data = await self._load()
        uid = str(user_id)
        data.setdefault(uid, [])
        data[uid] = [item for item in data[uid] if item.get("title") != title]
        await self._save(data)

    async def list(self, user_id: int) -> List[dict]:
        data = await self._load()
        return data.get(str(user_id), [])

    async def set(self, user_id: int, items: List[dict]):
        data = await self._load()
        data[str(user_id)] = items
        await self._save(data)



