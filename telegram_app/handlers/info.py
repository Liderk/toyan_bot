import asyncio

from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from telegram_app.config import settings
from telegram_app.filters.access_group import AccessGroupFilter
from telegram_app.filters.auth_filter import AuthFilter
from telegram_app.init_bot import bot
from telegram_app.keyboards.inline_info_kb import create_info_inline_kb
from telegram_app.orm.managers import EventManager
from telegram_app.orm.utils import get_nearest_game, get_nearest_event, get_games_by_current_month, \
    get_events_by_current_month
from telegram_app.utils.constants import Commands, MainKeyboardCommands, EventsInfo

info_router = Router()
info_router.message.filter(
    AccessGroupFilter(chat_type=["group", "supergroup"], allowed_group_chats=[settings.CHAT_ID, settings.GROUP_ID]),
)


async def get_nearest_event_data():
    event = await get_nearest_event()
    if event is None:
        return f'Ближайших мероприятий нет'
    event_type = EventManager.get_by_id(event.event_type)
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
            f'Командующий Тоян: {game.judas_commander}\n'
            f'Командующий стороны: {game.side_commander}')


async def get_data_for_games_by_current_month():
    games = await get_games_by_current_month()
    return '\n-----\n'.join([f'{game.name}, '
                             f'{game.start_date.strftime("%H:%M %d.%m.%Y")}, '
                             f'{game.city}' for game in games])


async def get_data_for_events_by_current_month():
    events = await get_events_by_current_month()

    return '\n-----\n'.join([f'{event.name}, '
                             f'{EventManager.get_by_id(event.event_type)}, '
                             f'{event.descriptions}, '
                             f'{event.start_date.strftime("%H:%M %d.%m.%Y")}'
                             for event in events])


INFO_MENU = {
    1: {Commands.INFO: EventsInfo.nearest_game, 'answer': get_nearest_game_data},
    2: {Commands.INFO: EventsInfo.nearest_event, 'answer': get_nearest_event_data},
    3: {Commands.INFO: EventsInfo.month_games, 'answer': get_data_for_games_by_current_month},
    4: {Commands.INFO: EventsInfo.month_event, 'answer': get_data_for_events_by_current_month},
}


@info_router.message(or_f((F.text == MainKeyboardCommands.INFO), Command(Commands.INFO)), AuthFilter())
async def init_info(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.type in ('group', 'supergroup'):
        await bot.send_message(chat_id=message.chat.id,
                               reply_to_message_id=message.message_thread_id,
                               reply_markup=create_info_inline_kb(INFO_MENU),
                               text='Что ты хочешь узнать?')
        return
    await message.answer('Что ты хочешь узнать?',
                         reply_markup=create_info_inline_kb(INFO_MENU))


@info_router.callback_query(F.data.startswith(f'{Commands.INFO}_'), AuthFilter())
async def info_detail(call: CallbackQuery):
    await call.answer()
    info_id = int(call.data.replace(f'{Commands.INFO}_', ''))
    info_data = INFO_MENU[info_id]
    data = await info_data.get('answer')()
    msg_text = f'<b>{info_data.get("info")}</b>\n\n' \
               f'{data}\n\n' \
               f'Что то еще, собака сутулая?'
    if not call.message.from_user.is_bot:
        async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
            await asyncio.sleep(2)
            await call.message.answer(msg_text, reply_markup=create_info_inline_kb(INFO_MENU))
            return

    await bot.send_message(chat_id=call.message.chat.id,
                           reply_to_message_id=call.message.message_thread_id,
                           text=msg_text)



