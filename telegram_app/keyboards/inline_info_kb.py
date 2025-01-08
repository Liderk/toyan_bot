from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_app.utils.constants import Commands


def create_info_inline_kb(info_menu: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for info_id, info_data in info_menu.items():
        builder.row(
            InlineKeyboardButton(
                text=info_data.get(Commands.INFO),
                callback_data=f'{Commands.INFO}_{info_id}'
            )
        )
    # Добавляем кнопку "На главную"
    builder.row(
        InlineKeyboardButton(
            text='На главную',
            callback_data='back_home'
        )
    )
    # Настраиваем размер клавиатуры
    builder.adjust(2)
    return builder.as_markup()
