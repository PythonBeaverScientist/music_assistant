import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from config import settings
from logger import logger
from utils.db_clients import mongo_client
from models.user import User, UserSettings

dp = Dispatcher()


def get_open_web_page_button():
    keyboard_button = KeyboardButton(text='Open Web Page', web_app=WebAppInfo(url=settings.WEB_APP_URL))
    return ReplyKeyboardMarkup(keyboard=[[keyboard_button,]])


def write_user_to_mongo_db(message: Message) -> str:

    user_settings = UserSettings(
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot,
        is_premium=message.from_user.is_premium
    )

    user = User(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        user_settings=user_settings
    )

    return user.post_unique(mongo_client)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    web_page_button = get_open_web_page_button()
    inserted_id = write_user_to_mongo_db(message)
    logger.error(f"USer with id: {inserted_id=} has made start request")
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! You are welcome to open web page",
        reply_markup=web_page_button
    )


async def main() -> None:
    bot = Bot(token=settings.BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Bot has been started')
    asyncio.run(main())
