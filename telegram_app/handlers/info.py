import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from config import settings
from filters.access_group import AccessGroupFilter
from filters.auth_filter import AuthFilter
from init_bot import bot
from keyboards.inline_info_kb import create_info_inline_kb, detail_inline_kb
from orm.managers import EventManager
from orm.utils import get_nearest_game, get_nearest_event, get_games_by_current_month, \
    get_events_by_current_month, get_all_upcoming_games, get_all_upcoming_events
from utils.constants import Commands, MainKeyboardCommands, EventsInfo, InfoExtendCommands

from utils.detailazers import GameDetailizer, EventDetailizer

from utils.common import send_message, process_send_detail_message

info_router = Router()
info_router.message.filter(
    AccessGroupFilter(chat_type=["group", "supergroup"], allowed_group_chats=[settings.CHAT_ID, settings.GROUP_ID]),
)


async def get_nearest_event_data():
    event = await get_nearest_event()
    if event is None:
        return f'Ближайших мероприятий нет'
    event_type = await EventManager.get_by_id(event.event_type)
    event_date = event.start_date.strftime('%H:%M %d.%m.%Y')
    return (f'Название: {event.name}\n'
            f'Тип события: {event_type}\n'
            f'Место: {event.location}\n'
            f'Описание: {event.descriptions}\n'
            f'Дата начала: {event_date}')


async def get_nearest_game_data():
    game = await get_nearest_game()
    if game is None:
        return f'Ближайших игр нет'
    start_date = game.start_date.strftime('%H:%M %d.%m.%Y')
    return (f'Название: {game.name}\n'
            f'Большая игра: {"Да" if game.big else "Нет"}\n'
            f'Дата начала: {start_date}\n'
            f'Город: {game.city}\n'
            f'Полигон: {game.game_area}\n'
            f'Командующий Тоян: {game.toyan_commander}\n'
            f'Командующий стороны: {game.side_commander}')


async def get_data_for_games_by_current_month():
    games = await get_games_by_current_month()
    return '\n-----\n'.join([f'{index}. {game.name}, '
                             f'{game.start_date.strftime("%H:%M %d.%m.%Y")}, '
                             f'{game.city}' for index, game in enumerate(games, start=1)])


async def get_data_for_all_games():
    games = await get_all_upcoming_games()
    return '\n-----\n'.join([f'{index}. {game.name}, '
                             f'{game.start_date.strftime("%H:%M %d.%m.%Y")}, '
                             f'{game.city}' for index, game in enumerate(games, start=1)])


async def get_data_for_events_by_current_month():
    events = await get_events_by_current_month()
    return '\n-----\n'.join([f'{index}. {event.name}, '
                             f'{await EventManager.get_by_id(event.event_type)}, '
                             f'{event.descriptions}, '
                             f'{event.start_date.strftime("%H:%M %d.%m.%Y")}'
                             for index, event in enumerate(events, start=1)])


async def get_data_for_all_upcoming_events():
    events = await get_all_upcoming_events()

    return '\n-----\n'.join([f'{index}. {event.name}, '
                             f'{await EventManager.get_by_id(event.event_type)}, '
                             f'{event.descriptions}, '
                             f'{event.start_date.strftime("%H:%M %d.%m.%Y")}'
                             for index, event in enumerate(events, start=1)])


class Form(StatesGroup):
    all_game_detail = State()
    all_event_detail = State()
    month_game_detail = State()
    month_event_detail = State()
    abort = State()


INFO_MENU = {
    1: {Commands.MENU: EventsInfo.nearest_game, 'answer': get_nearest_game_data, 'state': Form.abort},
    2: {Commands.MENU: EventsInfo.nearest_event, 'answer': get_nearest_event_data, 'state': Form.abort},
    3: {Commands.MENU: EventsInfo.month_games, 'answer': get_data_for_games_by_current_month,
        'state': Form.month_game_detail},
    4: {Commands.MENU: EventsInfo.month_event, 'answer': get_data_for_events_by_current_month,
        'state': Form.month_event_detail},
    5: {Commands.MENU: EventsInfo.upcoming_games, 'answer': get_data_for_all_games, 'state': Form.all_game_detail},
    6: {Commands.MENU: EventsInfo.upcoming_events, 'answer': get_data_for_all_upcoming_events,
        'state': Form.all_event_detail},
}


@info_router.message(F.text == MainKeyboardCommands.INFO, AuthFilter())
async def init_info(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.type in ('group', 'supergroup'):
        return
    await message.answer('Что ты хочешь узнать?',
                         reply_markup=create_info_inline_kb(INFO_MENU))


@info_router.callback_query(F.data.startswith(f'{Commands.MENU}_'), AuthFilter())
async def info_detail(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    info_id = int(call.data.replace(f'{Commands.MENU}_', ''))
    info_data = INFO_MENU[info_id]
    data = await info_data.get('answer')()
    msg_text = f'<b>{info_data.get(Commands.MENU)}</b>\n\n' \
               f'{data}\n\n' \
               f'Для подробной информации укажи цифру'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=detail_inline_kb())
    await state.set_state(info_data['state'])


@info_router.message(F.text, Form.month_game_detail)
async def detail_month_game(message: Message, state: FSMContext):
    result = await process_send_detail_message(get_games_by_current_month, message, GameDetailizer())
    if result:
        await state.clear()


@info_router.message(F.text, Form.all_game_detail)
async def detail_all_game(message: Message, state: FSMContext):
    result = await process_send_detail_message(get_all_upcoming_games, message, GameDetailizer())
    if result:
        await state.clear()


@info_router.message(F.text, Form.month_event_detail)
async def detail_month_event(message: Message, state: FSMContext):
    result = await process_send_detail_message(get_events_by_current_month, message, EventDetailizer())
    if result:
        await state.clear()


@info_router.message(F.text, Form.all_event_detail)
async def detail_all_event(message: Message, state: FSMContext):
    result = await process_send_detail_message(get_all_upcoming_events, message, EventDetailizer())
    if result:
        await state.clear()


@info_router.callback_query(F.data.startswith(InfoExtendCommands.abort_info_commands), AuthFilter())
async def abort_info(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Отменено')


@info_router.callback_query(F.data.startswith(InfoExtendCommands.come_back), AuthFilter())
async def come_back(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Что ты хочешь узнать?',
                              reply_markup=create_info_inline_kb(INFO_MENU))
