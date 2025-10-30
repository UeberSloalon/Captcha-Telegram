import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from bot.handlers import captcha


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.token)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(captcha.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())