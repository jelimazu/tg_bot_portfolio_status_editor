import asyncio
from aiogram import Bot, Dispatcher

from data.config import *
from data.database.db import check_db
from app.routers import register_all_routers
from app.middlewares import register_all_middlwares

from pyrogram import Client
from pyrogram.handlers import MessageHandler
from app.userbot.userbot_handlers import system_message_deleter

import data.config as config


async def main():
    await check_db()

    client = Client("my_account", api_id=config.api_id, api_hash=config.api_hash)
    client.add_handler(MessageHandler(system_message_deleter))
    await client.start()
    print("Userbot successfully started")

    bot = Bot(token=token, parse_mode="HTML")
    bot_info = await bot.get_me()
    await config.update_data(bot_info)
    dp = Dispatcher()
    register_all_middlwares(dp)
    register_all_routers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
        print('Exit')
