import sqlite3
import json
from typing import Optional, Dict, Any
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

class SQLiteStorage(BaseStorage):
    def __init__(self, path: str = "fsm_data.db"):
        self.conn = sqlite3.connect(path)
        self._create_table()

    #создание таблицы
    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS fsm (
                    chat_id INTEGER,
                    user_id INTEGER,
                    state TEXT,
                    data TEXT,
                    PRIMARY KEY (chat_id, user_id)
                )
            """)

    async def set_state(self, key: StorageKey, state: StateType = None):
        self._ensure_user_entry(key)
        with self.conn:
            self.conn.execute(
                "UPDATE fsm SET state = ? WHERE chat_id = ? AND user_id = ?",
                (state.state if state else None, key.chat_id, key.user_id)
            )

    #получение состояния
    async def get_state(self, key: StorageKey) -> Optional[str]:
        row = self.conn.execute(
            "SELECT state FROM fsm WHERE chat_id = ? AND user_id = ?",
            (key.chat_id, key.user_id)
        ).fetchone()
        return row[0] if row else None

    #сохранение данных
    async def set_data(self, key: StorageKey, data: Dict[str, Any]):
        self._ensure_user_entry(key)
        with self.conn:
            self.conn.execute(
                "UPDATE fsm SET data = ? WHERE chat_id = ? AND user_id = ?",
                (json.dumps(data), key.chat_id, key.user_id)
            )

    #извлечение данных
    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        row = self.conn.execute(
            "SELECT data FROM fsm WHERE chat_id = ? AND user_id = ?",
            (key.chat_id, key.user_id)
        ).fetchone()
        return json.loads(row[0]) if row and row[0] else {}

    #запись данных
    def _ensure_user_entry(self, key: StorageKey):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO fsm (chat_id, user_id, state, data) VALUES (?, ?, NULL, NULL)",
                (key.chat_id, key.user_id)
            )

    async def close(self) -> None:
        self.conn.close()

    async def get_user_count(self) -> int:
        cursor = self.conn.execute("SELECT COUNT(DISTINCT user_id) FROM fsm")
        row = cursor.fetchone()
        return row[0] if row else 0
