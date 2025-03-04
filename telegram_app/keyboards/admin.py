from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.constants import AdminKeyboardCommands


def create_admin_kb():
    builder = InlineKeyboardBuilder()

    keyboard_buttons = [
        InlineKeyboardButton(text='👥 Пользователи', callback_data=AdminKeyboardCommands.USERS),
        InlineKeyboardButton(text='🆕 Заявки на регистрацию', callback_data=AdminKeyboardCommands.REGISTRATION_REQUESTS),
        InlineKeyboardButton(text='📧 Рассылка в бот всем', callback_data=AdminKeyboardCommands.ALL_BROADCAST_TO_BOT),
        InlineKeyboardButton(text='💌 Рассылка командирам', callback_data=AdminKeyboardCommands.COMMANDER_BROADCAST),
        InlineKeyboardButton(text='💌💌 Рассылка командирам и ответственным',
                             callback_data=AdminKeyboardCommands.RESPONSIBLE_BROADCAST),
        InlineKeyboardButton(text='💬 Сообщение с комментариями в канал',
                             callback_data=AdminKeyboardCommands.CHANNEL_MESSAGE_WITH_COMMENT),
        InlineKeyboardButton(text='✉️ Сообщение без комментариев в канал',
                             callback_data=AdminKeyboardCommands.CHANNEL_MESSAGE_WITHOUT_COMMENT),

    ]

    for button in keyboard_buttons:
        builder.row(button)

    builder.adjust(2, 1)

    return builder.as_markup()


def cancel_btn():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Отмена',
                                                                       callback_data=AdminKeyboardCommands.CANSEL)]])
