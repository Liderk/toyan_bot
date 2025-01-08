from dataclasses import dataclass


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
    ALL_BROADCAST: str = 'all_broadcast'
    COMMANDER_BROADCAST: str = 'commander_broadcast'
    CANSEL: str = 'cansel_broadcast'
