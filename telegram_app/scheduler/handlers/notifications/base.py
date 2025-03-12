from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pytz
from aiogram.types import InputMediaDocument
from sqlalchemy import update, select, and_

from config import settings
from handlers.utils import InMemoryMessageIdStorage
from init_bot import bot
from orm.db_utils import async_session_factory
from orm.managers import ContentTypeManager
from orm.models import NotificationPeriod, Event, Games, GameEventNotification, PeriodChoices, RecipientType
from orm.utils import get_all_users_ids_for_broadcast
from utils.constants import MsgAction


class INotification(ABC):
    model: type[Event | Games] = None

    async def run(self):
        async for obj, notification_data in self.iter_obj():
            await self.process_send_message(obj, notification_data)
            await self.set_notification_mark(notification_data)

    @staticmethod
    def calculate_notification_date(obj: Event | Games,
                                    notification_period: NotificationPeriod) -> datetime:
        match notification_period.period:
            case PeriodChoices.HOURS:
                delta = timedelta(hours=notification_period.amount)
            case PeriodChoices.DAYS:
                delta = timedelta(days=notification_period.amount)
            case PeriodChoices.WEEK:
                delta = timedelta(weeks=notification_period.amount)
            case PeriodChoices.MONTH:
                delta = timedelta(days=notification_period.amount * 30)  # Приблизительно месяц
            case _:
                raise ValueError(f"Unknown period type: {notification_period.period}")

        return datetime.combine(obj.start_date - delta, datetime.min.time())

    async def iter_obj(self):
        today = datetime.combine(datetime.today(), datetime.min.time())
        content_type_id = await ContentTypeManager.get_by_name(self.model.__tablename__.replace('events_', ''))
        stmt = (
            select(self.model, NotificationPeriod, GameEventNotification)
            .join(GameEventNotification, GameEventNotification.object_id == self.model.id)
            .join(NotificationPeriod, GameEventNotification.notification_period_id == NotificationPeriod.id)
            .where(
                and_(GameEventNotification.notified == False,
                     GameEventNotification.content_type_id == content_type_id)
            )
        )

        async with async_session_factory() as session:
            results = await session.execute(stmt)
            results = results.all()

        for obj, notification_period, notification_data in results:
            notification_date = self.calculate_notification_date(obj, notification_period)
            if notification_date == today:
                yield obj, notification_data

    async def process_send_message(self, obj: (Event | Games), notification_data: GameEventNotification):
        message_text = self.prepare_message_text(obj)
        message_files = self.prepare_message_files(obj, message_text)
        chat_ids = await self.get_chat_ids(notification_data)
        for chat_id in chat_ids:
            await self.send_message(chat_id, message_text,
                                    message_files,
                                    message_with_comment=notification_data.allow_discussion)

    @abstractmethod
    def prepare_message_files(self, obj: (Event | Games), message_text: str) -> list[InputMediaDocument]:
        pass

    @abstractmethod
    def prepare_message_text(self, obj: (Event | Games)) -> str:
        pass

    @staticmethod
    async def send_message(chat_id: int, message_text: str, media: list[InputMediaDocument],
                           message_with_comment: bool = False) -> None:
        if media:
            msg_data = await bot.send_media_group(chat_id=chat_id, media=media)
        else:
            msg_data = await bot.send_message(chat_id=chat_id, text=message_text, parse_mode="HTML")

        if not message_with_comment:
            msg = msg_data[0]
            InMemoryMessageIdStorage.add_msg(msg.message_id, MsgAction.delete)

    @staticmethod
    async def set_notification_mark(notification_obj: GameEventNotification):
        stmt = (
            update(GameEventNotification)
            .where(GameEventNotification.id == notification_obj.id)
            .values(notified=True, notification_date=datetime.now(tz=pytz.timezone('Asia/Novosibirsk')))
        )
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_chat_ids(notification_data: GameEventNotification) -> list[int]:
        if notification_data.message_for == RecipientType.BOT:
            return await get_all_users_ids_for_broadcast(excluding_id=0)
        else:
            return [settings.CHAT_ID]
