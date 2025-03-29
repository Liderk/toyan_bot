from collections.abc import Generator, Callable
from datetime import datetime

import pytz
from aiogram.types import InputMediaDocument, Message

from config import settings
from handlers.utils import InMemoryMessageIdStorage
from init_bot import bot
from utils.constants import MsgAction

from utils.detailazers import IDetailizer


async def process_send_detail_message(obj_func: Callable, message: Message, msg_detailizer: IDetailizer):
    try:
        obj_index = int(message.text)
    except ValueError:
        await message.reply('Укажи только номер')
        return False

    objs = await obj_func()
    objs = {index: obj for index, obj in enumerate(objs, start=1)}
    if obj_index not in objs:
        await message.reply(f'Записи под номером {obj_index} не найдено')
        return False

    required_obj = objs[obj_index]
    msg_text = msg_detailizer.prepare_message_text(required_obj)
    msg_files = msg_detailizer.prepare_message_files(required_obj, msg_text)
    await send_message(message.chat.id, msg_text, msg_files)
    return True


async def send_message(chat_id: int, message_text: str, media: list[InputMediaDocument],
                       message_with_comment: bool = False) -> None:
    if media:
        msg_data = await bot.send_media_group(chat_id=chat_id, media=media)
    else:
        msg_data = await bot.send_message(chat_id=chat_id, text=message_text, parse_mode="HTML")

    if chat_id == settings.CHAT_ID and not message_with_comment:
        msg = msg_data[0]
        InMemoryMessageIdStorage.add_msg(msg.message_id, MsgAction.delete)


def format_datetime_to_project_tz_str(dt: datetime) -> str:
    """
    Приводит объект datetime к часовому поясу settings.PROJECT_TZ'
    и возвращает строку в формате 'дд-мм-ГГГГ ЧЧ:ММ'.

    Параметры:
        dt (datetime): Исходный объект datetime (может быть наивным или с часовым поясом)

    Возвращает:
        str: Дата и время в формате 'дд-мм-ГГГГ ЧЧ:ММ' (Asia/Novosibirsk)
    """
    nsk_tz = pytz.timezone(settings.PROJECT_TZ)

    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    dt_nsk = dt.astimezone(nsk_tz)

    return dt_nsk.strftime('%d-%m-%Y %H:%M')
