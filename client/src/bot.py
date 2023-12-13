import asyncio
import logging
import sys
import toml

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from .handlers import quests


config = toml.load("config.toml")
BOT_TOKEN = config["Telegram"]["BOT_TOKEN"]

dp = Dispatcher()


async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp.include_router(quests.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
