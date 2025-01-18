from sqlalchemy import select

from telegram_app.orm.db_sqlite_utils import async_session_factory
from telegram_app.orm.models import Team


class TeamManager:
    teams: dict[int, str] = {}

    @classmethod
    async def get_by_id(cls, identifier: int):
        if identifier not in cls.teams:
            await cls.load()

        return cls.teams.get(identifier)

    @classmethod
    async def load(cls):
        stmt = select(Team.id, Team.name)
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            for id_, name in result:
                cls.teams[int(id_)] = name


class EventManager:
    event_type: dict[int, str] = {}

    @classmethod
    def get_by_id(cls, id_: int):
        return cls.event_type.get(id_)

    @classmethod
    def add_event(cls, id_: int, name: str):
        cls.event_type[id_] = name


EventManager.add_event(1, 'Тренировка')
EventManager.add_event(2, 'Сбор')
