import asyncio
import logging
import os


from aiogram import types, Dispatcher, Router, F, Bot

from aiogram.filters.state import State, StatesGroup
from dotenv import load_dotenv

from handlers import start_handlers, join_handers, gifts_handlers, send_gifts

router = Router()



class FsmReg(StatesGroup):
    name = State()
    phone = State()


load_dotenv()


async def main():
    try:
        bot = Bot(token=os.getenv('TOKEN'))
        dp = Dispatcher()
        dp.include_routers(start_handlers.router, join_handers.router, gifts_handlers.router, send_gifts.router)
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print('Бот остановлен принудительно')


if __name__ == '__main__':
    asyncio.run(main())
