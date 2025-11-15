
import os

from DB.db_func import db_message_id

from aiogram import types, Dispatcher, Router, F, Bot
from aiogram.exceptions import TelegramBadRequest

from dotenv import load_dotenv



load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))


async def get_dell_message(chat_id):
    messages = db_message_id(chat_id)
    try:
        for one_message in messages:
            try:
                await bot.delete_message(chat_id, one_message)
            except TelegramBadRequest:
                pass
    except Exception as e:
        print(e)