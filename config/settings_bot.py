from pathlib import Path
from pydantic import (
    Field
)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    telegram_key: str = Field(validation_alias='bot_token')

    _env_path = Path(__file__).resolve().parent / '.env'
    model_config = SettingsConfigDict(env_file=str(_env_path),
                                      env_file_encoding="utf-8",
                                      extra="ignore"
                                      )

bot_config = Config()