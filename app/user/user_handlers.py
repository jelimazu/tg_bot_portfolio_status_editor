from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from data.database.db import *


router = Router()


@router.message(Command("start"))
async def start(message: Message):
    if not await get_user_exists(message.from_user.id):
        await add_user(message.from_user.id)
    await message.answer("Приветствую тебя в боте великого кодера Jelimazu")


@router.message()
async def echo(message: Message):
    await message.answer("Ты что-то хотел сказать? 🤨")
