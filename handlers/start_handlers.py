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

from DB.db_func import db_clear_message_id, db_add_message_id, db_add_new_user, db_check_name_second_name, db_add_name, \
    db_new_room, db_in_group, db_start, check_out_pass
from dell_message import get_dell_message
from keyboards.main_keyboard import main_markup, main_markup_2

router = Router()








@router.message(Command('start'))
async def get_start(mess: Message, state: FSMContext):
    await state.clear()
    check = db_start(mess.from_user.id)
    photo = FSInputFile('i.webp')
    if check is False:
        db_add_new_user(mess.from_user.id)
        photo = FSInputFile('i.webp')
        msg = await mess.answer_photo(photo=photo,caption='Привет, это приложение тайного Санты, для тебя и твоих друзей. Создай новую комнату или зайди по пригласительному коду,'
                                'нажав на кнопки ниже', reply_markup=main_markup)
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await mess.delete()
    elif check is True:
        try:

            msg = await mess.answer_photo(photo=photo, caption=f'C возвращением, {db_in_group(mess.from_user.id)}', reply_markup=main_markup_2)
        except Exception as e:
            msg = await mess.answer_photo(photo=photo,caption='С возвращением, вы еще не вошли ни в одну комнату', reply_markup=main_markup)
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await mess.delete()


class FsmName(StatesGroup):
    name = State()
    second_name = State()


class FsmRoom(StatesGroup):
    name = State()
    passwod = State()

@router.callback_query(F.data == 'new_room')
async def get_new_room(call: CallbackQuery, state: FSMContext):
    check_name = db_check_name_second_name(call.from_user.id)[0]
    if check_name['name'] is None:
        msg = await call.message.answer('Давай познакомимся, как тебя зовут?\n Можешь добавить к своему имени смайликов\n'
                                        ' *ВВЕДИТЕ СВОЕ ИМЯ, НЕ КОД КОМНАТЫ* :)', parse_mode='Markdown')
        await state.set_state(FsmName.name)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
    else:
        msg = await call.message.answer('Как назовем твою комнату?')
        await state.set_state(FsmRoom.name)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))

@router.message(FsmName.name, F.content_type == ContentType.TEXT)
async def get_name(mess: Message, state: FSMContext):
    if mess.text is not None:
        db_add_name(mess.from_user.id, mess.text)
        await state.clear()
        msg = await mess.answer('Как назовем твою комнату?')
        await state.set_state(FsmRoom.name)
        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await mess.delete()


@router.message(FsmRoom.name, F.content_type == ContentType.TEXT)
async def get_name(mess: Message, state: FSMContext):
    if mess.text is not None:
        await state.update_data(name=mess.text)

    msg = await mess.answer('А теперь придумай СЕКРЕТНЫЙ КОД и запиши его!')
    await state.set_state(FsmRoom.passwod)
    await get_dell_message(mess.from_user.id)
    db_clear_message_id(mess.from_user.id)
    db_add_message_id(mess.from_user.id, str(msg.message_id))
    await mess.delete()


@router.message(FsmRoom.passwod, F.content_type == ContentType.TEXT)
async def get_pass(mess: Message, state: FSMContext):
    check = check_out_pass(mess.text)
    print(check)
    if check is None:
        if mess.text is not None:
            data = await state.get_data()
            check_and_update = db_new_room(mess.from_user.id, data['name'], mess.text)
            if check_and_update is True:
                await state.clear()
                msg = await mess.answer(f'Вы создали комнату {data["name"]}, пароль {mess.text}, отправьте пригласительный код друзьям! не забудьте записать.', reply_markup=main_markup_2)
                await get_dell_message(mess.from_user.id)
                db_clear_message_id(mess.from_user.id)
                db_add_message_id(mess.from_user.id, str(msg.message_id))
                await mess.delete()
            else:
                msg = await mess.answer(
                    f'Такая комната уже существует, попробуйте другое название')

                await get_dell_message(mess.from_user.id)
                db_clear_message_id(mess.from_user.id)
                db_add_message_id(mess.from_user.id, str(msg.message_id))
                await state.clear()
                await state.set_state(FsmRoom.name)
                await mess.delete()
    else:
        msg = await mess.answer(
            f'Такой секретный код уже есть, придумайте другой')

        await get_dell_message(mess.from_user.id)
        db_clear_message_id(mess.from_user.id)
        db_add_message_id(mess.from_user.id, str(msg.message_id))
        await state.set_state(FsmRoom.passwod)
        await mess.delete()



@router.message(FsmName.name)
async def error_name(mess: Message, state: FSMContext):
    msg = await mess.answer('Вводить можно буквы, цифры и смайлики, введи снова!')
    await get_dell_message(mess.from_user.id)
    db_clear_message_id(mess.from_user.id)
    db_add_message_id(mess.from_user.id, str(msg.message_id))
    await state.set_state(FsmName.name)
    await mess.delete()


@router.message(FsmRoom.name)
async def error_name(mess: Message, state: FSMContext):
    msg = await mess.answer('Вводить можно буквы, цифры и смайлики, введи снова!')
    await get_dell_message(mess.from_user.id)
    db_clear_message_id(mess.from_user.id)
    db_add_message_id(mess.from_user.id, str(msg.message_id))
    await state.set_state(FsmRoom.name)
    await mess.delete()


@router.message(FsmRoom.passwod)
async def error_name(mess: Message, state: FSMContext):
    msg = await mess.answer('Вводить можно буквы, цифры и смайлики, введи снова!')
    await get_dell_message(mess.from_user.id)
    db_clear_message_id(mess.from_user.id)
    db_add_message_id(mess.from_user.id, str(msg.message_id))
    await state.set_state(FsmRoom.passwod)
    await mess.delete()


@router.callback_query(F.data == 'cancel')
async def get_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    db_add_new_user(call.from_user.id)
    check = db_start(call.from_user.id)
    if check is False:
        msg = await call.message.answer('Привет, это приложение тайного санты, для тебя и твоих друзей. Создай новую комнату или зайди по пригласительному коду,'
                                'нажав на кнопки ниже', reply_markup=main_markup)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
        await call.message.delete()
    elif check is True:
        try:
            msg = await call.message.answer(f'C возвращением, {db_in_group(call.from_user.id)}', reply_markup=main_markup_2)
        except Exception as e:
            msg = await call.message.answer(f'C возвращением, скорее заходи или создавай команаты!\n Друзья уже ждут вас.',
                                            reply_markup=main_markup)
        await get_dell_message(call.from_user.id)
        db_clear_message_id(call.from_user.id)
        db_add_message_id(call.from_user.id, str(msg.message_id))
        await call.message.delete()


@router.callback_query(F.data == 'help_razrab')
async def get_help(call: CallbackQuery, state: FSMContext):
    await state.clear()
    photo = FSInputFile('my_gift.webp')
    text = ('❤️🎁🌟 Если вам понравилось приложение поддержите разработчика на любую сумму ниже, он тоже хочет новый год\n'
            '[отправить подарок разработчику](https://www.tbank.ru/cf/5SxKISnK6Cj)')
    msg = await call.message.answer_photo(photo=photo, caption=text, parse_mode='Markdown', reply_markup=main_markup_2)
    await get_dell_message(call.from_user.id)
    db_clear_message_id(call.from_user.id)
    db_add_message_id(call.from_user.id, str(msg.message_id))