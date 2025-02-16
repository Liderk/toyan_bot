from abc import abstractmethod, ABC
from typing import Any

from sqlalchemy import select

from telegram_app.orm.db_sqlite_utils import async_session_factory
from telegram_app.orm.models import Team
from telegram_app.utils.constants import CommandRole, COMMANDER, COMMANDER_ASSISTANT, STORMTROOPER


class ManagerBase(ABC):

    @classmethod
    @abstractmethod
    async def load(cls):
        pass


class TeamManager(ManagerBase):
    items: dict[int, Any] = {}

    @classmethod
    async def get_by_id(cls, identifier: Any):
        if identifier not in cls.items:
            await cls.load()

        return cls.items.get(identifier)

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
    async def get_by_id(cls, identifier: Any):
        if identifier not in cls.items:
            await cls.load()

        return cls.items.get(identifier)

    @classmethod
    def get_by_id(cls, id_: int):
        return cls.items.get(id_)

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
    async def get_by_id(cls, identifier: Any):
        if identifier not in cls.items:
            await cls.load()

        return cls.items.get(identifier)

    @classmethod
    def add_role(cls, id_: int, role: CommandRole):
        cls.items[id_] = role

    @classmethod
    async def load(cls):
        cls.add_role(COMMANDER.marker, COMMANDER)
        cls.add_role(COMMANDER_ASSISTANT.marker, COMMANDER_ASSISTANT)
        cls.add_role(STORMTROOPER.marker, STORMTROOPER)
