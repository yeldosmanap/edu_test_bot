import os

import dotenv

# Load the variables from the .env file
dotenv.load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
BOT_TOKEN = '6519674458:AAHZ0XESfoZQ7ztUwUwU9TEdlPbtjtj2fVY'

print('Bot variables loaded successfully')