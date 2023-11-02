import asyncio

import dotenv
import psycopg2.pool
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from buttons import keyboard, backButtonMenuKeyboard, subjects
from variables import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT
)
print("Connected to database successfully")


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    username = message.from_user.username
    conn = connection_pool.getconn()
    cur = conn.cursor()

    try:
        cur.execute("SELECT u.username FROM users u WHERE u.username = %s;", (username,))
        usernameInDb = cur.fetchone()

        if usernameInDb is not None:
            await message.answer(f'Welcome back @{username}!', reply_markup=keyboard)
            return
        else:
            cur.execute("INSERT INTO users (username, date_signed_in) VALUES (%s, CURRENT_TIMESTAMP);", (username,))
            conn.commit()
            await message.answer(f'Welcome @{username} to our Telegram Bot for education!', reply_markup=keyboard)
    finally:
        cur.close()
        connection_pool.putconn(conn)


@dp.message()
async def select(message: types.Message):
    if message.text == 'Help':
        await message.answer(
            '''This bot is designed to help you learn and test your knowledge in different subjects. To get started, 
            simply select the subject you would like to study or test from the menu below.''')
    elif message.text == 'Start test':
        await start_test_handler(message)


@dp.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer(
        '''This bot is designed to help you learn and test your knowledge in different subjects. To get started, 
        simply select the subject you would like to study or test from the menu below.''',
        reply_markup=backButtonMenuKeyboard)


@dp.message(Command('start_test'))
async def start_test_handler(message: types.Message):
    # Select a subject to test
    await message.answer('Please select the subject you would like to test:', reply_markup=subjects)


async def main(bot_to_start):
    await dp.start_polling(bot_to_start)
    try:
        await asyncio.sleep(2)
    finally:
        await dp.stop_polling()


if __name__ == '__main__':
    asyncio.run(main(bot))
