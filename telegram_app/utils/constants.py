from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class Commands:
    START: str = 'start'
    REGISTER: str = 'register'
    INFO: str = 'info'
    MAIN_KEYBOARD: str = 'keyboard'


@dataclass
class MainKeyboardCommands:
    ABOUT: str = 'Что делает этот бот?'
    INFO: str = 'Получить инфу по играм/мероприятиям'
    ADMIN: str = '⚙️ Админ панель'


@dataclass
class AdminKeyboardCommands:
    USERS: str = 'users'
    BAN: str = 'ban'
    ALL_BROADCAST_TO_BOT: str = 'all_broadcast_from_bot'
    COMMANDER_BROADCAST: str = 'commander_broadcast'
    CHANNEL_MESSAGE_WITH_COMMENT: str = 'channel_message_with_comment'
    CHANNEL_MESSAGE_WITHOUT_COMMENT: str = 'channel_message_without_comment'
    CANSEL: str = 'cansel_broadcast'


@dataclass
class EventsInfo:
    nearest_game: str = 'Ближайшая игра'
    nearest_event: str = 'Ближайшее мероприятие'
    month_games: str = 'Игры в этом месяце'
    month_event: str = 'Мероприятия в этом месяце'


@dataclass
class MsgAction:
    delete: str = 'delete'


class CommandRole(NamedTuple):
    rank: str
    marker: int


COMMANDER = CommandRole('командир', 1)
COMMANDER_ASSISTANT = CommandRole('заместитель', 2)
STORMTROOPER = CommandRole('боец', 3)
