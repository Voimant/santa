import asyncio
import os
from datetime import time, timedelta
import datetime
from distutils.command.check import check

from aiogram import types, Dispatcher, Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from dotenv import load_dotenv
from setuptools.msvc import msvc14_get_vc_env

from DB.db_func import db_clear_message_id, db_add_message_id, db_add_new_user, db_check_name_second_name, db_add_name, \
    db_new_room, db_join_room, db_join_call_room, db_in_group
from dell_message import get_dell_message
from keyboards.main_keyboard import main_markup, my_party_markup, main_markup_2

router = Router()


class FsmJoin(StatesGroup):
    name = State()
    my_name = State()

@router.callback_query(F.data == 'join_room')
async def join_room(call: CallbackQuery, state: FSMContext):
    check_name = db_check_name_second_name(call.from_user.id)[0]
    if check_name['name'] is None:
        msg = await call.message.answer('ДАВАЙ ПОЗНАКОМИМСЯ, КАК ТЕБЯ ЗОВУТ? можешь добавить к своему имени смайликов'
                                        ' чтобы тебя точно узнали, конечно, если захочешь :)')
        await state.set_state(FsmJoin.my_name)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
    else:
        msg = await call.message.answer('Выбери существующую комнату или введи секретный код комнаты', reply_markup=my_party_markup(call.from_user.id))
        await state.set_state(FsmJoin.name)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))


@router.message(FsmJoin.my_name, F.content_type == ContentType.TEXT)
async def get_name(mess: Message, state: FSMContext):
    if mess.text is not None:
        db_add_name(mess.from_user.id, mess.text)
        await state.clear()
        msg = await mess.answer('Выбери существующую комнату или введи секретный код комнаты', reply_markup=my_party_markup(mess.from_user.id))
        await state.set_state(FsmJoin.name)
        await mess.delete()
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))


@router.message(FsmJoin.name, F.content_type == ContentType.TEXT)
async def join_new_room(mess: Message, state: FSMContext):
    join_room = db_join_room(mess.from_user.id, mess.text)
    if join_room is not False:
        try:
            msg = await mess.answer(f'Вы присоединились к комнате *{join_room[0]}*. Загадайте желание Тайному Санте'
                                    f'а потом вы можете создать комнату для другой компании', reply_markup=main_markup_2, parse_mode='Markdown')
        except Exception as e:
            msg = await mess.answer(f'Такой комнаты нет, скорее заходи или создавай свою комнату!\n Друзья уже ждут тебя!.',
                                            reply_markup=main_markup)
        await state.clear()
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await mess.delete()
    else:
        msg = await mess.answer('У вас уже есть эта комната или ее не существует', reply_markup=main_markup_2)
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await mess.delete()
        await state.clear()



@router.callback_query(FsmJoin.name)
async def join_call_group(call: CallbackQuery, state: FSMContext):
    print(call.data)
    if call.data != 'cancel':
        db_join_call_room(call.from_user.id, call.data)
        msg = await call.message.answer(f'Вы перешли в комнату {call.data}', reply_markup=main_markup_2)
        await state.clear()
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
    elif call.data == 'cancel':
        msg = await call.message.answer('Вы вышли в главное меню\n'
                                        f'{db_in_group(call.from_user.id)}', reply_markup=main_markup_2)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))