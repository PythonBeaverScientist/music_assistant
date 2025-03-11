import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from config import settings
from logger import logger

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard_button = KeyboardButton(text='Open Web Page', web_app=WebAppInfo(url=settings.WEB_APP_URL))
    markup = ReplyKeyboardMarkup(keyboard=[[keyboard_button,]])
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! You are welcome to open web page",
        reply_markup=markup
    )


async def main() -> None:
    bot = Bot(token=settings.BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Bot has been started')
    asyncio.run(main())
