import asyncio
import logging
import sys
import toml

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from . import api


config = toml.load("config.toml")
BOT_TOKEN = config["Telegram"]["BOT_TOKEN"]

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    quests = await api.get_quests_list()

    kb = [[KeyboardButton(text=q.title)] for q in quests]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    for q in quests:
        await message.answer(q.get_quest_info(), reply_markup=markup)


async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    print("Starting the polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
