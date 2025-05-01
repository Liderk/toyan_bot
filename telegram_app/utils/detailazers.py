import os

from aiogram.types import InputMediaDocument, BufferedInputFile

from config import settings
from orm.models import Games, Event, EventChoices
from scheduler.handlers.notifications.utils import file_to_byte
from utils.common import format_datetime_to_project_tz_str
from utils.detailizer_interface import IDetailizer


class GameDetailizer(IDetailizer):
    def prepare_message_text(self, obj: Games) -> str:
        start_date = format_datetime_to_project_tz_str(obj.start_date)
        end_date = format_datetime_to_project_tz_str(obj.end_date)
        return (
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

        if game.location_map:
            map_file = os.path.join(settings.MEDIA_ROOT, game.location_map)
            media_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(map_file), map_file))
            files.append(media_file)

        if game.game_map:
            map_file = os.path.join(settings.MEDIA_ROOT, game.game_map)
            media_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(map_file), map_file),
                                            caption=message_text)
            files.append(media_file)

        if game.gpx:
            file_path = os.path.join(settings.MEDIA_ROOT, game.gpx)
            gpx_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(gpx_file)

        if game.kmz:
            file_path = os.path.join(settings.MEDIA_ROOT, game.kmz)
            kmz_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(kmz_file)

        if game.kml:
            file_path = os.path.join(settings.MEDIA_ROOT, game.kml)
            kml_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(kml_file)

        return files


class EventDetailizer(IDetailizer):
    def prepare_message_text(self, obj: Event) -> str:
        start_date = format_datetime_to_project_tz_str(obj.start_date)
        end_date = format_datetime_to_project_tz_str(obj.end_date)
        return (
            f"🔫 <b>Название события:</b> {obj.name}\n"
            f"📝 <b>Описание:</b> {obj.descriptions}\n"
            f"📅 <b>Дата начала:</b> {start_date}\n"
            f"📅 <b>Дата окончания:</b> {end_date}\n"
            f"👤 <b>Организаторы:</b> {obj.organizers}\n"
            f"📍 <b>Место проведения:</b> {obj.location}\n"
            f"🔍 <b>Тип события:</b> {'Тренировка' if obj.event_type == EventChoices.TRAINING  else 'Собрание'}"
        )

    def prepare_message_files(self, obj: Event, message_text: str) -> list[InputMediaDocument]:
        files = []

        if obj.location_map:
            map_file = os.path.join(settings.MEDIA_ROOT, obj.location_map)
            media_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(map_file), map_file),
                                            caption=message_text)
            files.append(media_file)

        if obj.gpx:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.gpx)
            gpx_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(gpx_file)

        if obj.kmz:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.kmz)
            kmz_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(kmz_file)

        if obj.kml:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.kml)
            kml_file = InputMediaDocument(media=BufferedInputFile(file_to_byte(file_path), file_path))
            files.append(kml_file)

        return files
