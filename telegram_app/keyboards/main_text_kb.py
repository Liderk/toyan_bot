from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from orm.utils import get_admin_ids
from utils.constants import MainKeyboardCommands


async def create_main_text_kb(user_id: int):
    admin_ids = await get_admin_ids()
    kb_list = [
        [KeyboardButton(text=MainKeyboardCommands.ABOUT)],
        [KeyboardButton(text=MainKeyboardCommands.INFO)],
        [KeyboardButton(text=MainKeyboardCommands.ADMIN_Q)],
    ]
    if user_id in admin_ids:
        kb_list.append([KeyboardButton(text=MainKeyboardCommands.ADMIN)])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
