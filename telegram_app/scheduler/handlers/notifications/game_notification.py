from orm.models import Games
from scheduler.handlers.notifications.base import INotification
from utils.common import format_datetime_to_project_tz_str
from utils.detailazers import GameDetailizer


class GameNotificator(GameDetailizer, INotification):
    model: type[Games] = Games

    def prepare_message_text(self, obj: Games) -> str:
        start_date = format_datetime_to_project_tz_str(obj.start_date)
        msg = super(GameDetailizer).prepare_message_text(obj)
        return f'Напоминаю, что {start_date} состоится игра:\n' + msg
