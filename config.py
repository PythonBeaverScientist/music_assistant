from pathlib import Path

import yaml
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    BOT_API_TOKEN: str = 'bot_api_token'
    LOG_CONFIG_PATH: str = 'logging.yml'

    LOG_CONFIG: dict = {}

    @field_validator('LOG_CONFIG', mode='before')
    @classmethod
    def load_conf_path(cls, v: str, info: ValidationInfo) -> dict:
        with Path(info.data.get("LOG_CONFIG_PATH", "logging.yml")).open() as file:
            return yaml.safe_load(file)


settings = Settings()
