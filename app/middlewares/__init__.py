# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from app.middlewares.middleware_throttling import ThrottlingMiddleware


# Регистрация всех миддлварей
def register_all_middlwares(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())