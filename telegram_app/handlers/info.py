import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from telegram_app.init_bot import bot
from telegram_app.keyboards.inline_info_kb import create_info_inline_kb
from telegram_app.orm.utils import get_nearest_game, get_nearest_event, get_games_by_current_month, \
    get_events_by_current_month
from telegram_app.utils.constants import Commands, MainKeyboardCommands

info_router = Router()


async def get_nearest_event_data():
    event = await get_nearest_event()
    return f'{event.name}, {event.event_type}, {event.descriptions}, {event.start_date}'


async def get_nearest_game_data():
    game = await get_nearest_game()
    return f'{game.name}, {game.start_date}, {game.city}'


async def get_data_for_games_by_current_month():
    games = await get_games_by_current_month()

    return '\n'.join([f'{game.name}, {game.start_date}, {game.city}' for game in games])


async def get_data_for_events_by_current_month():
    events = await get_events_by_current_month()

    return '\n'.join([f'{event.name}, {event.event_type}, {event.descriptions}, {event.start_date}'
                      for event in events])


INFO_MENU = {
    1: {Commands.INFO: 'Ближайшая игра', 'answer': get_nearest_game_data},
    2: {Commands.INFO: 'Ближайшее мероприятие', 'answer': get_nearest_event_data},
    3: {Commands.INFO: 'Игры в этом месяце', 'answer': get_data_for_games_by_current_month},
    4: {Commands.INFO: 'Мероприятия в этом месяце', 'answer': get_data_for_events_by_current_month},
}


@info_router.message(F.text == MainKeyboardCommands.INFO)
async def init_info(message: Message):
    await message.answer('Что ты хочешь узнать?',
                         reply_markup=create_info_inline_kb(INFO_MENU))


@info_router.callback_query(F.data.startswith(f'{Commands.INFO}_'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    info_id = int(call.data.replace(f'{Commands.INFO}_', ''))
    info_data = INFO_MENU[info_id]
    data = await info_data.get('answer')()
    msg_text = f'<b>{info_data.get("info")}</b>\n\n' \
               f'{data}\n\n' \
               f'Что то еще, собака сутулая?'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_info_inline_kb(INFO_MENU))
