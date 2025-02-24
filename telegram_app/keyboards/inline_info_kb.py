from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..utils.constants import Commands


def create_info_inline_kb(info_menu: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for info_id, info_data in info_menu.items():
        builder.row(
            InlineKeyboardButton(
                text=info_data.get(Commands.MENU),
                callback_data=f'{Commands.MENU}_{info_id}'
            )
        )
    # Настраиваем размер клавиатуры
    builder.adjust(2, 1)
    return builder.as_markup()
