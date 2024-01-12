import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from app.admin.admin_keyboard import *

import data.database.db as db
from data.config import *
import data.config as config

router = Router()


class AdminState(StatesGroup):
    set_status_name = State()
    set_status_photo = State()
    edit_status_name = State()
    edit_status_photo = State()


@router.message(Command("admin"))
async def admin(message: Message):
    await message.answer("Вы вошли в админ панель", reply_markup=admin_keyboard())
    try:
        await message.delete()
    except:
        pass


@router.callback_query(F.data == "statuses")
async def statuses(call: CallbackQuery):
    await call.message.edit_text("🌐 Статусы", reply_markup=await statuses_keyboard())
    await call.answer()


@router.callback_query(F.data.startswith("use_status"))
async def use_status(call: CallbackQuery):
    status_id = call.data.split(":")[1]
    status = await db.get_status(status_id)
    status_m_id = await db.get_message_id_for_statuses()
    if status_m_id != 0:
        await call.bot.set_chat_photo(config.channel_username, FSInputFile(f"pics/{status[0]}.png"))
        await call.bot.edit_message_text(chat_id=config.channel_username, message_id=status_m_id,
                                         text=f"Текущий статус: {status[1]}")
        await call.answer("Статус успешно установлен")
        await db.set_current_status(status_id)
        await call.message.edit_reply_markup(reply_markup=await statuses_keyboard())
    else:
        await call.answer("Сначала отправьте сообщение со статусом")


@router.callback_query(F.data == "admin_menu")
async def admin_menu(call: CallbackQuery):
    await call.message.edit_text("Вы вошли в админ панель", reply_markup=admin_keyboard())
    await call.answer()


@router.callback_query(F.data == "settings")
async def settings(call: CallbackQuery):
    await call.message.edit_text("💋 Настройка статусов", reply_markup=settings_keyboard())
    await call.answer()


@router.callback_query(F.data == "add_status")
async def add_status(call: CallbackQuery, state: FSMContext):
    m = await call.message.edit_text("🖊 Введите название статуса который хотите добавить",
                                     reply_markup=cancel_keyboard())
    await state.set_state(AdminState.set_status_name)
    await state.update_data(m_id=m.message_id)


@router.message(F.text, AdminState.set_status_name)
async def set_status_name(message: Message, state: FSMContext):
    status_name = message.text
    data = await state.get_data()
    m_id = data.get("m_id")
    try:
        await message.delete()
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass
    m = await message.answer(f"Статус: {status_name}\n\nОтправьте фото для статуса", reply_markup=cancel_keyboard())
    await state.set_state(AdminState.set_status_photo)
    await state.update_data(status_name=status_name, m_id=m.message_id)


@router.message(F.photo, AdminState.set_status_photo)
async def set_status_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    status_name = data.get("status_name")
    m_id = data.get("m_id")
    photo_id = message.photo[-1].file_id
    status_id = await db.add_status(status_name, photo_id)
    await message.bot.download(message.photo[-1], destination=f"pics/{status_id}.png")
    try:
        await message.delete()
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass
    await message.answer("✅ Статус успешно добавлен", reply_markup=admin_keyboard())


@router.callback_query(F.data == "edit_statuses")
async def edit_statuses(call: CallbackQuery):
    await call.message.edit_text("⚙️ Редактировать статусы", reply_markup=await edit_statuses_keyboard())
    await call.answer()


@router.callback_query(F.data.startswith("edit_status"))
async def edit_status(call: CallbackQuery):
    status_id = call.data.split(":")[1]
    status = await db.get_status(status_id)
    await call.message.answer_photo(photo=status[2], caption=f"Статус: {status[1]}",
                                    reply_markup=edit_status_keyboard(status_id))
    await call.answer()


@router.callback_query(F.data.startswith("edit_name_status"))
async def edit_status_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    status_id = call.data.split(":")[1]
    m_main_id = call.message.message_id
    m = await call.message.answer("🖊 Введите новое название статуса", reply_markup=cancel_keyboard())
    await state.set_state(AdminState.edit_status_name)
    await state.update_data(status_id=status_id, m_id=m.message_id, m_main_id=m_main_id)


@router.message(F.text, AdminState.edit_status_name)
async def edit_status_name(message: Message, state: FSMContext):
    data = await state.get_data()
    status_id = data.get("status_id")
    m_id = data.get("m_id")
    m_main_id = data.get("m_main_id")
    status_name = message.text
    await db.edit_status_name(status_id, status_name)
    try:
        await message.delete()
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass
    try:
        await message.bot.edit_message_caption(chat_id=message.chat.id, message_id=m_main_id,
                                               caption=f"Статус: {status_name}",
                                               reply_markup=edit_status_keyboard(status_id))
    except:
        pass


@router.callback_query(F.data.startswith("edit_photo_status"))
async def edit_status_photo(call: CallbackQuery, state: FSMContext):
    await call.answer()
    status_id = call.data.split(":")[1]
    m_main_id = call.message.message_id
    m = await call.message.answer("🖊 Отправьте новое фото статуса", reply_markup=cancel_keyboard())
    await state.set_state(AdminState.edit_status_photo)
    await state.update_data(status_id=status_id, m_id=m.message_id, m_main_id=m_main_id)


@router.message(F.photo, AdminState.edit_status_photo)
async def edit_status_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    status_id = data.get("status_id")
    m_id = data.get("m_id")
    m_main_id = data.get("m_main_id")
    photo_id = message.photo[-1].file_id
    await db.edit_status_photo(status_id, photo_id)
    status = await db.get_status(status_id)
    try:
        os.remove(f"pics/{status_id}.png")
        await message.bot.download(message.photo[-1], destination=f"pics/{status_id}.png")
    except:
        await message.answer("Не удалось удалить старое фото")
        return None
    try:
        await message.delete()
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass
    try:
        await message.bot.edit_message_media(chat_id=message.chat.id, message_id=m_main_id,
                                             media=InputMediaPhoto(media=photo_id, caption=f"Статус: {status[1]}"),
                                             reply_markup=edit_status_keyboard(status_id))
        # await message.bot.edit_message_caption(chat_id=message.chat.id, message_id=m_main_id,
        #                                        caption=f"Статус: {status[1]}",
        #                                        reply_markup=edit_status_keyboard(status_id))
    except:
        pass


@router.callback_query(F.data.startswith("delete_status"))
async def delete_status(call: CallbackQuery):
    status_id = call.data.split(":")[1]
    await db.delete_status(status_id)
    try:
        os.remove(f"pics/{status_id}.png")
    except:
        pass
    await call.answer("Статус успешно удален")
    await call.message.delete()


@router.callback_query(F.data == "send_message_status")
async def send_message_status(call: CallbackQuery):
    try:
        m = await call.bot.send_message(config.channel_username, "Текущий статус: Не установлен")
        await db.set_message_id_for_statuses(m.message_id)
        await call.answer("Сообщение успешно отправлено")
    except Exception as e:
        await call.answer("Не удалось отправить сообщение: " + str(e))


@router.callback_query(F.data == "close")
async def cancel(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()

