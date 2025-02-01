from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_main_inline_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
                text='Получить инфу по играм/мероприятиям',
                callback_data='Получить инфу по играм/мероприятиям'
            ),
    )
    builder.adjust(1)
    builder = InlineKeyboardBuilder()