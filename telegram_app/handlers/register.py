import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from telegram_app.init_bot import bot
from telegram_app.orm.utils import create_inactive_user, find_user_by_telegram_id
from telegram_app.utils.constants import Commands

register_router = Router()


class Form(StatesGroup):
    username = State()
    team = State()
    is_commander = State()


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
    await state.set_state(Form.username)


@register_router.message(F.text, Form.username)
async def capture_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Команда: ')
    await state.set_state(Form.team)


@register_router.message(F.text, Form.team)
async def capture_team(message: Message, state: FSMContext):
    await state.update_data(team=message.text)
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

    await state.update_data(is_commander=message.text)

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        data = await state.get_data()

        msg_text = (f'Позывной: <b>{data.get("username")}</b>, \n'
                    f'Команда: <b>{data.get("team")}</b>, \n'
                    f'Командир: <b>{data.get("is_commander")}</b>. \n\n'
                    f'Заявка на регистрацию принята.')

        data['is_commander'] = data['is_commander'] == 'да'
        data['telegram_id'] = message.from_user.id

        await create_inactive_user(data)

        await message.answer(msg_text)
        await message.answer('Продолжайте вести наблюдение, мы с вами свяжемся.')
    await state.clear()
