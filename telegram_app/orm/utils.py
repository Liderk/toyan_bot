import random
import string
from datetime import datetime, timedelta

import pytz
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError

from telegram_app.orm.db_sqlite_utils import async_session_factory
from telegram_app.orm.models import TelegramUser, Event, Games


async def get_admin_ids():
    stmt = select(TelegramUser.telegram_id).where(TelegramUser.is_active == True,
                                                  TelegramUser.is_admin == True)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def find_user_by_telegram_id(telegram_id: int) -> TelegramUser | None:
    stmt = select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def create_inactive_user(user_data: dict):
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))
    new_user = TelegramUser(**user_data, date_joined=now)
    async with async_session_factory() as session:
        try:
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            username = f'{user_data["username"]}_{"".join(random.choices(string.ascii_letters + string.digits, k=6))}'
            new_user.username = username
            session.add(new_user)
        await session.commit()
        return new_user


async def get_nearest_event() -> Event | None:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))
    stmt = select(Event).order_by(Event.start_date).filter(Event.start_date >= now).limit(1)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_nearest_game() -> Games | None:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))
    stmt = select(Games).order_by(Games.start_date).filter(Games.start_date >= now).limit(1)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_events_by_current_month() -> list[Event]:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))

    end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)

    stmt = select(Event).order_by(Event.start_date).filter(
        and_(Event.start_date >= now, Event.start_date <= end_of_month)
    )
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_games_by_current_month() -> list[Games]:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))

    end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)

    stmt = select(Games).order_by(Games.start_date).filter(
        and_(Games.start_date >= now, Games.start_date <= end_of_month)
    )
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_all_users_ids_for_broadcast(excluding_id: int):
    stmt = select(TelegramUser.telegram_id).where(TelegramUser.is_active == True,
                                                  TelegramUser.telegram_id.isnot(excluding_id))

    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_commander_users_ids_for_broadcast(excluding_id: int):
    stmt = select(TelegramUser.telegram_id).where(TelegramUser.is_active == True,
                                                  TelegramUser.telegram_id.isnot(excluding_id),
                                                  TelegramUser.is_commander == True)

    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()
