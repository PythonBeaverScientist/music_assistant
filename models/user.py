from models.common import BaseMongoModel, UserSettings, Field


class User(BaseMongoModel):

    def __init__(
            self, telegram_id: int, username: str, full_name: str, user_settings: UserSettings
    ):
        self.telegram_id = Field(int, telegram_id, is_primary_key=True)
        self.username = Field(str, username)
        self.full_name = Field(str, full_name)
        self.settings = Field(dict, user_settings.value)

        super().__init__()
