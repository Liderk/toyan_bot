from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_app.utils.constants import AdminKeyboardCommands


def create_admin_kb():
    builder = InlineKeyboardBuilder()

    keyboard_buttons = [
        InlineKeyboardButton(text='👥 Пользователи', callback_data=AdminKeyboardCommands.USERS),
        InlineKeyboardButton(text='💀 Бан пользователя', callback_data=AdminKeyboardCommands.BAN),
        InlineKeyboardButton(text='📧 Общая рассылка', callback_data=AdminKeyboardCommands.ALL_BROADCAST),
        InlineKeyboardButton(text='💌 Рассылка ответственным', callback_data=AdminKeyboardCommands.COMMANDER_BROADCAST),
    ]

    for button in keyboard_buttons:
        builder.row(button)

    builder.adjust(2, 2)

    return builder.as_markup()


def cancel_btn():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Отмена',
                                                                       callback_data=AdminKeyboardCommands.CANSEL)]])
