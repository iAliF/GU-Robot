import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')  # Api Bot Token
CHANNEL = os.getenv('CHANNEL')  # The bot should be admin in this channel
INTERVAL = int(os.getenv('INTERVAL'))  # In minutes
