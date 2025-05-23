import logging
from collections.abc import Callable
from datetime import datetime

import pytz
from aiogram.types import InputMediaDocument, Message

from config import settings
from handlers.utils import InMemoryMessageIdStorage
from init_bot import bot
from utils.constants import MsgAction
from utils.detailizer_interface import IDetailizer

logger = logging.getLogger(__name__)


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
    await simple_send_detail_message(required_obj, message, msg_detailizer)


async def simple_send_detail_message(obj, message: Message, msg_detailizer: IDetailizer):
    msg_text = msg_detailizer.prepare_message_text(obj)
    msg_files = msg_detailizer.prepare_message_files(obj, message_text=f'Файлы к {obj.name}')
    await send_message(message.chat.id, msg_text, msg_files)
    return True


async def send_message(chat_id: int, message_text: str, media: list[InputMediaDocument],
                       message_with_comment: bool = False) -> None:
    if chat_id == settings.CHAT_ID:
        await send_message_to_channel(message_text, media, message_with_comment)

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode="HTML")

    if media:
        await bot.send_media_group(chat_id=chat_id, media=media)


async def send_message_to_channel(message_text: str, media: list[InputMediaDocument],
                                  message_with_comment: bool = False) -> None:
    msg_data = await bot.send_message(chat_id=settings.CHAT_ID, text=message_text, parse_mode="HTML")
    msg = msg_data[0]

    if not message_with_comment:
        InMemoryMessageIdStorage.add_msg(msg.message_id, MsgAction.delete)
        return None

    if media:
        try:
            await bot.send_media_group(
                chat_id=settings.GROUP_ID,
                media=media,
                reply_to_message_id=msg.message_id
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке медиафайлов: {e}")


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
