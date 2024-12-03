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
    db_new_room, db_join_room, db_join_call_room, db_in_group, db_gifts_check, db_gifts, db_kakashka, db_kaka, my_name, \
    my_gift_friend, db_checkout_gifts
from dell_message import get_dell_message
from keyboards.main_keyboard import main_markup, my_party_markup, main_markup_2, cancel_markup

router = Router()

class FsmGifts(StatesGroup):
    text = State()


@router.callback_query(F.data == 'my_gifts')
async def get_gifts(call: CallbackQuery, state: FSMContext):
    await state.clear()
    check = db_gifts_check(call.from_user.id)
    photo = FSInputFile('gift.webp')
    print(check)
    status_game = db_checkout_gifts(call.from_user.id)[0]
    print(status_game)
    if status_game is not True:
        if check ==  (None,):
            msg = await call.message.answer_photo(photo=photo,caption='Опишите словами свое желание подробно,'
                                        ' что бы Санте было проще найти именно то что вам нужно', reply_markup=cancel_markup)
            await get_dell_message(call.from_user.id)
            db_clear_message_id(call.from_user.id)
            db_add_message_id(call.from_user.id, str(msg.message_id))
            await state.set_state(FsmGifts.text)
        else:
            text = (f'Ваше желание сейчас:\n\n'
                    f'{check[0]}\n\n'
                    f'Хотите загадать другое? если да просто напишите и отправьте')
            msg = await call.message.answer_photo(photo=photo,caption=text, reply_markup=cancel_markup)
            await get_dell_message(call.from_user.id)
            db_clear_message_id(call.from_user.id)
            db_add_message_id(call.from_user.id, str(msg.message_id))
            await state.set_state(FsmGifts.text)
    else:
        msg = await call.message.answer_photo(photo=photo, caption='Игра уже проведена, подарок изменить невозможно!', reply_markup=main_markup_2)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
        await state.clear()

@router.message(FsmGifts.text, F.content_type == ContentType.TEXT)
async def get_go_gifts(mess: Message, state: FSMContext):
    db_gifts(mess.from_user.id, mess.text)
    photo = FSInputFile('gift_1.webp')
    msg = await mess.answer_photo(photo=photo, caption='Я передам ваше желание санте! Спасибо за участие :)', reply_markup=main_markup_2)
    await mess.delete()
    await get_dell_message(mess.from_user.id)
    db_clear_message_id(mess.from_user.id)
    db_add_message_id(mess.from_user.id, str(msg.message_id))
    await state.clear()

@router.callback_query(F.data == 'no_gifts')
async def no_gifts(call: CallbackQuery, state: FSMContext):
    await state.clear()
    result = db_kaka(db_kakashka(call.from_user.id)[0])
    text = ''
    for one in result:
        if one['gift'] == '' or one['gift'] is None:
            name = my_name(one['user_id'])
            text += f'💩 *{name[0]}* ничего не попросил у Санты\n\n'

        else:
            name = my_name(one['user_id'])
            text +=f'✅ *{name[0]}* загадал подарок\n\n'
    msg = await call.message.answer(f'Доска почета:\n\n {text}\n\n *Всего участников:* {len(result)}', parse_mode='Markdown', reply_markup=main_markup_2)
    await get_dell_message(call.from_user.id)
    db_clear_message_id(call.from_user.id)
    db_add_message_id(call.from_user.id, str(msg.message_id))


@router.callback_query(F.data == 'why')
async def get_my_friend_gift(call: CallbackQuery, state: FSMContext):
    await state.clear()
    gift = my_gift_friend(call.from_user.id)
    text = (f'Кто ждет от вас подарок: \n🤩 *{gift[0]}*\n\n'
            f'Подарок:\n'
            f'{gift[1]}')
    msg = await call.message.answer(text, reply_markup=main_markup_2, parse_mode='Markdown')
    await get_dell_message(call.from_user.id)
    db_clear_message_id(call.from_user.id)
    db_add_message_id(call.from_user.id, str(msg.message_id))