from orm.models import Event
from scheduler.handlers.notifications.base import INotification
from utils.common import format_datetime_to_project_tz_str
from utils.detailazers import EventDetailizer


class EventNotificator(EventDetailizer, INotification):
    model: type[Event] = Event

    def prepare_message_text(self, obj: Event) -> str:
        start_date = format_datetime_to_project_tz_str(obj.start_date)
        msg = super(EventDetailizer).prepare_message_text(obj)
        return f'Напоминаю, что {start_date} состоится событие:\n' + msg
