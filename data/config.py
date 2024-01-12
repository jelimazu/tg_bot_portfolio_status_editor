import configparser

from aiogram.types import User

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.txt')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8')
data = config["settings"]
token = data["token"]
channel_username = data["channel_username"]
admin_id = list(map(int, data["admin_id"].split(",")))
api_id = data["api_id"]
api_hash = data["api_hash"]
bot_username = str
bot_name = str


async def update_data(user: User):
    global bot_username
    global bot_name

    bot_username = user.username
    bot_name = user.first_name
    print(f"@{bot_username}", bot_name)
