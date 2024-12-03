from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from DB.db_func import my_party_list

main_button = [
    [InlineKeyboardButton(text='🎄 Создать комнату', callback_data='new_room')],
    [InlineKeyboardButton(text='🎄 Войти в комнату', callback_data='join_room')],
]
main_markup = InlineKeyboardMarkup(inline_keyboard=main_button)


main_button_2 = [
    [InlineKeyboardButton(text='🎄 Создать комнату', callback_data='new_room')],
    [InlineKeyboardButton(text='🎄 Поменять комнату', callback_data='join_room')],
    [InlineKeyboardButton(text='🎁Загадать желание Тайному санте', callback_data='my_gifts')],
    [InlineKeyboardButton(text='💩 Кому уголек? кто не загадал желание?', callback_data='no_gifts')],
    [InlineKeyboardButton(text='🎁🌟 Кому и что я дарю?', callback_data='why')],
    [InlineKeyboardButton(text='❤️🎁🌟 Поддержать разработчика', callback_data='help_razrab')]

]
main_markup_2 = InlineKeyboardMarkup(inline_keyboard=main_button_2)


send_button = [
    [InlineKeyboardButton(text='Кому и что я дарю?', callback_data='why')],
    [InlineKeyboardButton(text='🎄 Главное меню', callback_data='cancel')]
]

cancel_button = [[InlineKeyboardButton(text='🎄 Главное меню', callback_data='cancel')]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=cancel_button)

# main_room = [
#     [InlineKeyboardButton(text='Загадать желание тайному санте', callback_data='my_surprise')],
#     [InlineKeyboardButton(text='Посмотреть кому и что дарю', callback_data='prew')],
#     [InlineKeyboardButton(text='написать анонимное сообщение', callback_data='my_rooms')],
#     [InlineKeyboardButton(text='Кто еще не загадал подарок?', callback_data='my_rooms')],
# ]
# main_room_markup = InlineKeyboardMarkup(inline_keyboard=main_room)

def my_party_markup(chat_id):
    list_cats = my_party_list(chat_id)
    builder = InlineKeyboardBuilder()
    for cat in list_cats:
        builder.button(text=f'🌟{cat}', callback_data=cat)
    builder.button(text='🌟 В главное меню', callback_data='cancel')
    builder.adjust(1)
    return builder.as_markup()
