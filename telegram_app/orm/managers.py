from abc import abstractmethod, ABC
from dataclasses import dataclass, astuple
from typing import Any

from sqlalchemy import select

from orm.db_utils import async_session_factory
from orm.models import Team, Event, Games, ContentType
from utils.constants import CommandRole, COMMANDER, COMMANDER_ASSISTANT, STORMTROOPER


class ManagerBase(ABC):
    items: dict[int, Any] = None

    @classmethod
    @abstractmethod
    async def load(cls):
        pass

    @classmethod
    async def get_by_id(cls, identifier: Any):
        if identifier not in cls.items:
            await cls.load()

        return cls.items.get(identifier)


class TeamManager(ManagerBase):
    items: dict[int, Any] = {}

    @classmethod
    async def load(cls):
        stmt = select(Team.id, Team.name)
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            for id_, name in result:
                cls.items[int(id_)] = name


class EventManager(ManagerBase):
    items: dict[int, Any] = {}

    @classmethod
    def add_event(cls, id_: int, name: str):
        cls.items[id_] = name

    @classmethod
    async def load(cls):
        cls.add_event(1, 'Тренировка')
        cls.add_event(2, 'Сбор')


class CommandRoleManager(ManagerBase):
    items: dict[int, Any] = {}

    @classmethod
    def add_role(cls, id_: int, role: CommandRole):
        cls.items[id_] = role

    @classmethod
    async def load(cls):
        cls.add_role(COMMANDER.marker, COMMANDER)
        cls.add_role(COMMANDER_ASSISTANT.marker, COMMANDER_ASSISTANT)
        cls.add_role(STORMTROOPER.marker, STORMTROOPER)


@dataclass
class TableName:
    EVENT: str = Event.__tablename__.replace('events_', '')
    GAME: str = Games.__tablename__.replace('events_', '')


class ContentTypeManager:
    items: dict[str, int] = {}

    @classmethod
    async def get_by_name(cls, identifier: str):
        if identifier not in cls.items:
            await cls.load()

        return cls.items.get(identifier)

    @classmethod
    async def load(cls):
        async with async_session_factory() as session:
            for name in astuple(TableName()):
                stmt = select(ContentType).where(ContentType.model == name)
                result = await session.execute(stmt)
                obj = result.scalar()
                cls.items[name] = obj.id
