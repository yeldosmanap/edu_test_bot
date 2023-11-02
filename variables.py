# Load variables from .env file
import dotenv

variables = dotenv.get_variables('.env')

# Access the variables
DATABASE_NAME = variables.get('DATABASE_NAME')
DATABASE_USER = variables.get('DATABASE_USER')
DATABASE_PASSWORD = variables.get('DATABASE_PASSWORD')
DATABASE_HOST = variables.get('DATABASE_HOST')
DATABASE_PORT = variables.get('DATABASE_PORT')
BOT_TOKEN = '6519674458:AAHZ0XESfoZQ7ztUwUwU9TEdlPbtjtj2fVY'
print('Bot variables loaded successfully')