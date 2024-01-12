import aiosqlite
import datetime
from os import system

import pytz

path = "data/database/database.db"


async def check_db() -> None:
    system("cls")
    _datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        try:
            await cursor.execute("SELECT * FROM users")
            print("----   Database was found   ----")
        except aiosqlite.OperationalError:
            print("----   Database not found   ----")
        print(f"-----   {_datetime}   -----")


def get_now_date() -> str:
    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Kiev")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y")
    return format_date


def get_now_time() -> str:
    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Kiev")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y %H:%M")
    return format_date


async def get_user_exists(user_id) -> bool:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user = await cursor.fetchone()
        if user is None:
            return False
        else:
            return True


async def add_user(user_id) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"INSERT INTO users (user_id, reg_date) VALUES ({user_id}, '{get_now_date()}')")
        await db.commit()


async def get_message_id_for_statuses() -> int:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT m_id FROM settings")
        m_id = await cursor.fetchone()
        return m_id[0]


async def set_message_id_for_statuses(m_id) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE settings SET m_id = {m_id}")
        await db.commit()


async def get_current_status() -> int:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT current_status_id FROM settings")
        status_id = await cursor.fetchone()
        return status_id[0]


async def set_current_status(status_id) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE settings SET current_status_id = {status_id}")
        await db.commit()


async def add_status(status_name, photo_id) -> int:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"INSERT INTO statuses (name, photo_id) VALUES ('{status_name}', '{photo_id}')")
        await db.commit()
        await cursor.execute(f"SELECT * FROM statuses WHERE name = '{status_name}'")
        status = await cursor.fetchone()
        return status[0]


async def get_all_statuses() -> list:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM statuses")
        statuses = await cursor.fetchall()
        return statuses


async def get_status(status_id) -> tuple:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM statuses WHERE id = {status_id}")
        status = await cursor.fetchone()
        return status


async def edit_status_name(status_id, new_name) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE statuses SET name = '{new_name}' WHERE id = {status_id}")
        await db.commit()


async def edit_status_photo(status_id, new_photo_id) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE statuses SET photo_id = '{new_photo_id}' WHERE id = {status_id}")
        await db.commit()


async def delete_status(status_id) -> None:
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"DELETE FROM statuses WHERE id = {status_id}")
        await db.commit()
