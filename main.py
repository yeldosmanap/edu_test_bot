import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '6519674458:AAHGTFRO6JKuh2czJc8WGgP9zXR7RHaMC8Y'
bot = Bot(token=TOKEN)
dp = Dispatcher()

helpButton = KeyboardButton(text='Help')
startTestButton = KeyboardButton(text='Start test')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[helpButton, startTestButton]])

backButtonMenu = KeyboardButton(text='Back to menu')
# Welcome message
@dp.message(CommandStart())
async def welcome(message: types.Message) -> None:
    username = message.from_user.username
    await message.answer(f'Welcome @{username} to our Telegram Bot for education!', reply_markup=keyboard)


@dp.message()
async def select(message: types.Message) -> None:
    if message.text == 'Help':
        await message.answer(
            '''This bot is designed to help you learn and test your knowledge in different subjects. To get started, 
            simply select the subject you would like to study or test from the menu below.''')
    elif message.text == 'Start test':
        await start_test(message)


# Help menu
@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer(
        '''This bot is designed to help you learn and test your knowledge in different subjects. To get started, 
        simply select the subject you would like to study or test from the menu below.''',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[backButtonMenu]]))


# Start test menu
@dp.message(Command('start_test'))
async def start_test(message: types.Message):
    # Create a keyboard with the different subjects to choose from
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Computer Science')
    keyboard.add('Mathematics')
    keyboard.add('English')
    keyboard.add('Physics')

    # Send the keyboard to the user
    await message.answer('Please select the subject you would like to test:', reply_markup=keyboard)


# Statistics menu
@dp.message(Command('statistics'))
async def statistics(message: types.Message):
    # Create a keyboard with the different subjects to choose from
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Computer Science')
    keyboard.add('Mathematics')
    keyboard.add('English')
    keyboard.add('Physics')

    await message.answer('Please select the subject you would like to see your statistics for:', reply_markup=keyboard)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
