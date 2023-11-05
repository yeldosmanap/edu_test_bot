from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

print('Initializing buttons...')
# Main menu keyboard
helpButton = KeyboardButton(text='Help', callback_data='help')
startTestButton = KeyboardButton(text='Start test', callback_data='start_test')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[helpButton, startTestButton]])

# Back to menu button
backButtonMenuKeyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
    InlineKeyboardButton(text='Back to menu', callback_data='back_to_menu')
]])

# Subjects keyboard with 4 buttons for each subject
subjects = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
    KeyboardButton(text='Computer Science', callback_data='computer_science'),
    KeyboardButton(text='Mathematics', callback_data='mathematics'),
    KeyboardButton(text='English', callback_data='english'),
    KeyboardButton(text='Physics', callback_data='physics'),
    KeyboardButton(text='Go menu', callback_data='start'),
]])
