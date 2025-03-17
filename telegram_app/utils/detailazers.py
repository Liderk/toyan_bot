import os
from abc import abstractmethod, ABC

from aiogram.types import InputMediaDocument, BufferedInputFile

from config import settings
from orm.models import Games, Event, EventChoices
from scheduler.handlers.notifications.utils import file_to_byte


class IDetailizer(ABC):
    @abstractmethod
    def prepare_message_text(self, obj: (Games, Event)) -> str:
        pass

    @abstractmethod
    def prepare_message_files(self, game: (Games, Event), message_text: str) -> list:
        pass


class GameDetailizer(IDetailizer):
    def prepare_message_text(self, obj: Games) -> str:
        return (
            f"🔫 <b>Название игры:</b> {obj.name}\n"
            f"📝 <b>Описание:</b> {obj.descriptions}\n"
            f"📅 <b>Дата начала:</b> {obj.start_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📅 <b>Дата окончания:</b> {obj.end_date.strftime('%Y-%m-%d %H:%M')}\n"
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

        return files


class EventDetailizer(IDetailizer):
    def prepare_message_text(self, obj: Event) -> str:
        return (
            f"🔫 <b>Название события:</b> {obj.name}\n"
            f"📝 <b>Описание:</b> {obj.descriptions}\n"
            f"📅 <b>Дата начала:</b> {obj.start_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📅 <b>Дата окончания:</b> {obj.end_date.strftime('%Y-%m-%d %H:%M')}\n"
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

        return files
