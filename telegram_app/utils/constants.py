from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class Commands:
    START: str = 'start'
    REGISTER: str = 'register'
    MENU: str = 'menu'
    MAIN_KEYBOARD: str = 'keyboard'


@dataclass
class MainKeyboardCommands:
    ABOUT: str = 'Что делает этот бот?'
    INFO: str = 'Получить инфу по играм/мероприятиям'
    ADMIN: str = '⚙️ Админ панель'
    ADMIN_Q: str = 'Написать админу'


@dataclass
class AdminKeyboardCommands:
    USERS: str = 'users'
    REGISTRATION_REQUESTS: str = 'registration_requests'
    ALL_BROADCAST_TO_BOT: str = 'all_broadcast_from_bot'
    COMMANDER_BROADCAST: str = 'commander_broadcast'
    RESPONSIBLE_BROADCAST: str = 'responsible_broadcast'
    CHANNEL_MESSAGE_WITH_COMMENT: str = 'channel_message_with_comment'
    CHANNEL_MESSAGE_WITHOUT_COMMENT: str = 'channel_message_without_comment'
    CANSEL: str = 'cansel_broadcast'


@dataclass
class EventsInfo:
    nearest_game: str = 'Ближайшая игра'
    nearest_event: str = 'Ближайшее мероприятие'
    month_games: str = 'Игры в этом месяце'
    month_event: str = 'Мероприятия в этом месяце'
    upcoming_games: str = 'Все предстоящие игры'
    upcoming_events: str = 'Все предстоящие мероприятия'


@dataclass
class MsgAction:
    delete: str = 'delete'


class CommandRole(NamedTuple):
    rank: str
    marker: int


COMMANDER = CommandRole('командир', 1)
COMMANDER_ASSISTANT = CommandRole('заместитель', 2)
STORMTROOPER = CommandRole('боец', 3)
