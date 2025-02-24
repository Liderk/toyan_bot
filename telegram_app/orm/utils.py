import random
import string
from datetime import datetime, timedelta

import pytz
import sqlalchemy
from sqlalchemy import select, and_, update, or_
from sqlalchemy.exc import IntegrityError

from ..orm.db_utils import async_session_factory
from ..orm.models import TelegramUser, Event, Games, Team


async def get_admin_ids():
    stmt = select(TelegramUser.telegram_id).where(TelegramUser.is_active == True,
                                                  TelegramUser.is_admin == True)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_admins():
    stmt = select(TelegramUser).where(TelegramUser.is_active == True,
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


async def get_all_upcoming_games() -> list[Games]:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))
    stmt = select(Games).order_by(Games.start_date).filter(Games.start_date >= now)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_events_by_current_month() -> list[Event]:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))

    end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)

    stmt = select(Event).order_by(Event.start_date).filter(
        and_(Event.start_date >= now, Event.start_date <= end_of_month)
    )
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_all_upcoming_events() -> list[Games]:
    now = datetime.now(tz=pytz.timezone('Asia/Novosibirsk'))
    stmt = select(Event).order_by(Event.start_date).filter(Event.start_date >= now)
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


async def get_commander(excluding_id: int):
    stmt = select(TelegramUser).where(
        TelegramUser.is_active == True,
        TelegramUser.telegram_id.isnot(excluding_id),
        TelegramUser.is_commander == True)

    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_commander_and_responsible_person(excluding_id: int):
    stmt = select(TelegramUser).where(
        TelegramUser.is_active == True,
        TelegramUser.telegram_id.isnot(excluding_id),
        or_(
            TelegramUser.is_commander == True,
            TelegramUser.responsible_person == True,
        )
    )

    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def ban_user(telegram_id: int):
    stmt = update(TelegramUser).where(TelegramUser.telegram_id == telegram_id).values(is_banned=True)
    async with async_session_factory() as session:
        await session.execute(stmt)
        await session.commit()


async def get_teams_with_users():
    async with async_session_factory() as session:
        # Запрашиваем все команды и их участников за один запрос
        result = await session.execute(
            select(Team).options(
                sqlalchemy.orm.selectinload(Team.telegram_users)
            ).order_by(Team.id)
        )
        teams = result.scalars().all()
        return teams


async def get_registration_requests():
    stmt = select(TelegramUser).where(TelegramUser.is_active == False)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().all()
