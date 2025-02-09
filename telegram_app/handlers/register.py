import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from telegram_app.init_bot import bot
from telegram_app.orm.managers import TeamManager
from telegram_app.orm.utils import create_inactive_user, find_user_by_telegram_id, get_admin_ids, get_admins
from telegram_app.utils.constants import Commands

register_router = Router()


class Form(StatesGroup):
    callsign = State()
    team = State()
    is_commander = State()
    responsible_person = State()


@register_router.message(Command(Commands.REGISTER))
async def start_registration(message: Message, state: FSMContext):
    await state.clear()
    user = await find_user_by_telegram_id(message.from_user.id)

    if user and user.is_active:
        await message.answer('Ты уже зарегистрирован')
        return
    if user and not user.is_active:
        await message.answer('Заявка на регистрацию на рассмотрении. Ожидай!')
        return

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Твой позывной: ')
    await state.set_state(Form.callsign)


@register_router.message(F.text, Form.callsign)
async def capture_username(message: Message, state: FSMContext):
    await state.update_data(callsign=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        msg = f'Выбери свою команду (укажи номер):\n'
        await TeamManager.load()
        for team_id, name in TeamManager.teams.items():
            msg = msg + f'{team_id} - {name}\n'
        await message.answer(msg)
    await state.set_state(Form.team)


@register_router.message(F.text, Form.team)
async def capture_team(message: Message, state: FSMContext):
    try:
        command_id = int(message.text)
    except ValueError:
        await message.reply('Укажи только номер команды')
        return

    if not await TeamManager.get_by_id(command_id):
        await message.reply('Указанный номер команды не существует. Укажи правильный')
        return

    await state.update_data(team_id=command_id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Ты командир? (да/нет): ')
    await state.set_state(Form.is_commander)


@register_router.message(F.text, Form.is_commander)
async def capture_commander(message: Message, state: FSMContext):
    answer = message.text.lower()

    if answer not in ('да', 'нет'):
        await message.reply('Ответь да или нет')
        return
    await state.update_data(is_commander=message.text.lower())

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Ты ответственное лицо в команде(зам командира и т.д.)? (да/нет)\n'
                             'Если ты командир, то ответь тут тоже да. ')

    await state.set_state(Form.responsible_person)


@register_router.message(F.text, Form.responsible_person)
async def responsible_person(message: Message, state: FSMContext):
    answer = message.text.lower()

    if answer not in ('да', 'нет'):
        await message.reply('Ответь да или нет')
        return

    await state.update_data(responsible_person=message.text.lower())

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        data = await state.get_data()
        team = await TeamManager.get_by_id(data.get('team_id'))
        msg_text = (f'Позывной: <b>{data.get("callsign")}</b>, \n'
                    f'Команда: <b>{team}</b>, \n'
                    f'Командир: <b>{data.get("is_commander")}</b>. \n'
                    f'Ответственное лицо: <b>{data.get("responsible_person")}</b>. \n\n'
                    f'Заявка на регистрацию принята.')

        data['is_commander'] = data['is_commander'] == 'да'
        data['responsible_person'] = data['responsible_person'] == 'да'
        data['telegram_id'] = message.from_user.id
        data['telegram_username'] = message.from_user.username

        await create_inactive_user(data)

        await message.answer(msg_text)
        await message.answer('Продолжайте вести наблюдение, мы с вами свяжемся.')

        admins_ids = await get_admin_ids()
        for admin_id in admins_ids:
            await bot.send_message(chat_id=admin_id,
                                   text=f'Новая заявка на регистрацию:\n{msg_text}')

    await state.clear()
