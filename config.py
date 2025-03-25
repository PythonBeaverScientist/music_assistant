from pathlib import Path

import yaml
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR_PATH = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file= CURRENT_DIR_PATH / '.env', env_file_encoding='utf-8', extra='ignore')

    BOT_API_TOKEN: str = 'bot_api_token'
    WEB_APP_URL: str = 'web_app_url'
    LOG_CONFIG_PATH: str = 'logging.yml'

    MONGO_INITDB_ROOT_USERNAME: str = ''
    MONGO_INITDB_ROOT_PASSWORD: str = ''
    MONGO_INITDB_DATABASE: str = ''

    LOG_CONFIG: dict = {}
    MONGO_URI: str = 'mongodb'

    @field_validator('LOG_CONFIG', mode='before')
    @classmethod
    def load_conf_path(cls, v: str, info: ValidationInfo) -> dict:
        log_path = info.data.get("LOG_CONFIG_PATH", "logging.yml")
        with Path(f"{CURRENT_DIR_PATH}/{log_path}").open() as file:
            return yaml.safe_load(file)

    @field_validator('MONGO_URI', mode='before')
    @classmethod
    def set_mongo_uri(cls, v: str, info: ValidationInfo) -> str:
        return (f"mongodb://{info.data.get('MONGO_INITDB_ROOT_USERNAME')}:"
                f"{info.data.get('MONGO_INITDB_ROOT_PASSWORD')}@localhost:27017/")



settings = Settings()
