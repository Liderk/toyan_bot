import os

from aiogram.types import InputMediaDocument, BufferedInputFile

from config import settings
from orm.models import Event, EventChoices
from scheduler.handlers.notifications.base import INotification
from scheduler.handlers.notifications.utils import file_to_byte


class EventNotificator(INotification):
    model: type[Event] = Event

    def prepare_message_text(self, obj: Event) -> str:
        return (
            f"Напоминаю, что {obj.start_date.strftime('%Y-%m-%d %H:%M')} состоится событие:\n"
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
