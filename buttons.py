from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

print('Initializing buttons...')
# Create a keyboard with a help button and a start test button
helpButton = KeyboardButton(text='Help')
startTestButton = KeyboardButton(text='Start test')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[helpButton, startTestButton]])

# Create a keyboard with a button to go back to the menu
backButtonMenu = KeyboardButton(text='Back to menu')
backButtonMenuKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[backButtonMenu]])

# Create a keyboard with the different subjects to choose from
subjects = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[]])

# Create buttons
computer_science_button = KeyboardButton(text='Computer Science', callback_data='computer_science')
mathematics_button = KeyboardButton(text='Mathematics', callback_data='mathematics')
english_button = KeyboardButton(text='English', callback_data='english')
physics_button = KeyboardButton(text='Physics', callback_data='physics')

# Add buttons to the keyboard
subjects.keyboard.append([computer_science_button])
subjects.keyboard.append([mathematics_button])
subjects.keyboard.append([english_button])
subjects.keyboard.append([physics_button])
