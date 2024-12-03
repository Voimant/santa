import asyncio
import os
from datetime import time, timedelta
import datetime
from distutils.command.check import check
import random
from aiogram import types, Dispatcher, Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from dotenv import load_dotenv

from DB.db_func import db_clear_message_id, db_add_message_id, db_add_new_user, db_check_name_second_name, db_add_name, \
    db_new_room, db_in_group, db_start, db_kakashka, db_kaka, my_role, reslut_game, db_in_group_id, my_gift_friend, \
    db_true_result, db_checkout_gifts
from dell_message import get_dell_message
from keyboards.main_keyboard import main_markup, main_markup_2

router = Router()

bot = Bot(token=os.getenv('TOKEN'))

@router.message(Command('santa'))
async def get_santa(mess: Message):
    my_roles = my_role(mess.from_user.id)
    if my_roles[0] == 'admin':
        status_game = db_checkout_gifts(mess.from_user.id)[0]
        if status_game[0] is not True:
            result = db_kaka(db_kakashka(mess.from_user.id)[0])
            list_chat_id = []
            for one in result:
                list_chat_id.append(one['user_id'])
            random.shuffle(list_chat_id)
            room_id = db_in_group_id(mess.from_user.id)[0]
            db_true_result(mess.from_user.id)
            # Инициализация пустого списка для пар
            pairs = []

            # Проходим по всем элементам списка
            for i in range(len(list_chat_id)):
                # Создаем пару из текущего элемента и следующего
                # Если текущий элемент последний, соединяем его с первым
                pairs.append([list_chat_id[i], list_chat_id[(i + 1) % len(list_chat_id)]])
            # Выводим результат
            for x in pairs:
                reslut_game(x[0],x[1], room_id)
                info = my_gift_friend(x[0])
                text = (f'🎁 Новый год начинается! от вас ждет подарок \n {info[0]}\n'
                        f'💌 Письмо от вашего друга:\n {info[1]}\n'
                        f'💃💃💃Комната в которой загадал подарок: {info[2]}')
                await bot.send_message(x[0], text, reply_markup=main_markup_2)
            print(list_chat_id)
            print(pairs)
        else:
            await mess.answer('Игра уже проведена, невозможно провести еще раз', reply_markup=main_markup_2)



