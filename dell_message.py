import asyncio
import os
from datetime import time, timedelta
import datetime
from difflib import diff_bytes
from distutils.util import execute
from sre_parse import parse
from urllib.request import CacheFTPHandler

from aiogram.enums import ContentType
from aiohttp.web_routedef import delete

from DB.db_func import db_message_id

from aiogram import types, Dispatcher, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from pydantic.v1.validators import anystr_strip_whitespace
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