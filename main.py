import asyncio
import logging

import psycopg2.pool
from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from config import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, BOT_TOKEN


class Form(StatesGroup):
    START_TEST = State()
    SUBJECT = State()
    QUESTIONS = State()
    ANSWER = State()


subject_filter = StateFilter(Form.SUBJECT)

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT
)
print("Connected to database successfully")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(handlers.router)
    await dp.start_polling(bot)
    try:
        await asyncio.sleep(2)
    finally:
        await dp.stop_polling()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
