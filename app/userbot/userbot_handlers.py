import pyrogram
from pyrogram.enums import MessageServiceType

from data.config import channel_username


async def system_message_deleter(client: pyrogram.Client, message: pyrogram.types.Message):
    if message.chat.username and message.chat.username in channel_username and message.service == MessageServiceType.NEW_CHAT_PHOTO:
        await message.delete()
