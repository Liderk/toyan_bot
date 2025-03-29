import os

from aiogram.types import BufferedInputFile, InputMediaDocument

from config import settings

from orm.models import Games
from scheduler.handlers.notifications.base import INotification
from scheduler.handlers.notifications.utils import file_to_byte
from utils.common import format_datetime_to_project_tz_str


class GameNotificator(INotification):
    model: type[Games] = Games

    def prepare_message_text(self, obj: Games) -> str:
        start_date = format_datetime_to_project_tz_str(obj.start_date)
        end_date = format_datetime_to_project_tz_str(obj.end_date)
        return (
            f"Напоминаю, что {start_date} состоится игра:\n"
            f"🔫 <b>Название игры:</b> {obj.name}\n"
            f"📝 <b>Описание:</b> {obj.descriptions}\n"
            f"📅 <b>Дата начала:</b> {start_date}\n"
            f"📅 <b>Дата окончания:</b> {end_date}\n"
            f"👤 <b>Организаторы:</b> {obj.organizers}\n"
            f"🏙️ <b>Город:</b> {obj.city}\n"
            f"📍 <b>Место проведения:</b> {obj.game_area}\n"
            f"⚔️ <b>Командир стороны:</b> {obj.side_commander or 'Не указан'}\n"
            f"⚔️ <b>Командир Тояна:</b> {obj.toyan_commander or 'Не указан'}\n"
            f"🔍 <b>Масштаб игры:</b> {'Крупная' if obj.big else 'Небольшая'}"
        )

    def prepare_message_files(self, game: Games, message_text: str) -> list:
        files = []

        if game.game_map:
            map_file = os.path.join(settings.MEDIA_ROOT, game.game_map)
            media_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(map_file), map_file),
                                            caption=message_text)
            files.append(media_file)
        if game.location_map:
            map_file = os.path.join(settings.MEDIA_ROOT, game.location_map)
            media_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(map_file), map_file))
            files.append(media_file)

        return files
