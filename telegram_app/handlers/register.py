import asyncio
from copy import deepcopy
from curses.ascii import isdigit

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from ..init_bot import bot
from ..orm.managers import TeamManager, CommandRoleManager
from ..orm.utils import create_inactive_user, find_user_by_telegram_id, get_admin_ids, get_admins
from ..utils.constants import Commands, COMMANDER, COMMANDER_ASSISTANT

register_router = Router()


class Form(StatesGroup):
    callsign = State()
    team = State()
    command_role = State()


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
        for team_id, name in TeamManager.items.items():
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
        await CommandRoleManager.load()
        choices = '\n'.join(f'{role.marker}: {role.rank}' for role in CommandRoleManager.items.values())
        await message.answer(f'Кто ты:\n{choices}')
    await state.set_state(Form.command_role)


@register_router.message(F.text, Form.command_role)
async def capture_commander(message: Message, state: FSMContext):
    marker = message.text.strip()
    try:
        isdigit(marker)
    except TypeError:
        choices = '\n'.join(f'{role.marker}: {role.rank}' for role in CommandRoleManager.items.values())
        await message.reply(f'Просто поставь нужную цифру:\n{choices}')
        return

    await state.update_data(command_role=int(marker))

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        data = await state.get_data()
        team = await TeamManager.get_by_id(data.get('team_id'))
        team_role = await CommandRoleManager.get_by_id(data.get('command_role'))
        msg_text = (f'Позывной: <b>{data.get("callsign")}</b>, \n'
                    f'Команда: <b>{team}</b>, \n'
                    f'Роль в команде: <b>{team_role.rank}</b>. \n\n'
                    f'Заявка на регистрацию принята.')

        data['is_commander'] = data['command_role'] == COMMANDER.marker
        data['responsible_person'] = data['command_role'] == COMMANDER_ASSISTANT.marker
        data['telegram_id'] = message.from_user.id
        data['telegram_username'] = message.from_user.username or f'{message.from_user.full_name}'

        model_data = deepcopy(data)
        del model_data['command_role']

        await create_inactive_user(model_data)

        await message.answer(msg_text)
        await message.answer('Продолжайте вести наблюдение, мы с вами свяжемся.')

        admins_ids = await get_admin_ids()
        for admin_id in admins_ids:
            await bot.send_message(chat_id=admin_id,
                                   text=f'Новая заявка на регистрацию:\n{msg_text}')

    await state.clear()
