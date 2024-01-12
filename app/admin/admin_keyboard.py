from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import data.database.db as db


def admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🌐 Статусы", callback_data=f"statuses"),
        ],
        [
            InlineKeyboardButton(text="💋 Настройка статусов", callback_data=f"settings"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def statuses_keyboard() -> InlineKeyboardMarkup:
    statuses = await db.get_all_statuses()
    current_status_id = await db.get_current_status()
    buttons = []
    for status in statuses:
        if status[0] == current_status_id:
            buttons.append([InlineKeyboardButton(text=f"🔅 {status[1]}", callback_data=f"use_status:{status[0]}")])
        else:
            buttons.append([InlineKeyboardButton(text=f"{status[1]}", callback_data=f"use_status:{status[0]}")])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data=f"admin_menu")])
    buttons.append([InlineKeyboardButton(text="❌", callback_data=f"close")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def settings_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📝 Добавить статус", callback_data=f"add_status"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Редактировать статусы", callback_data=f"edit_statuses"),
        ],
        [
            InlineKeyboardButton(text="💬 Оставить сообщение со статусом", callback_data=f"send_message_status"),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data=f"admin_menu"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def edit_statuses_keyboard() -> InlineKeyboardMarkup:
    statuses = await db.get_all_statuses()
    buttons = []
    for status in statuses:
        buttons.append([InlineKeyboardButton(text=f"{status[1]}", callback_data=f"edit_status:{status[0]}")])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data=f"settings")])
    buttons.append([InlineKeyboardButton(text="❌", callback_data=f"close")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_status_keyboard(status_id: int | str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📝 Изменить название", callback_data=f"edit_name_status:{status_id}"),
            InlineKeyboardButton(text="📝 Изменить фото", callback_data=f"edit_photo_status:{status_id}"),
        ],
        [
            InlineKeyboardButton(text="🗑 Удалить статус", callback_data=f"delete_status:{status_id}"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
