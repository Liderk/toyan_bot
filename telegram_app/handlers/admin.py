from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from ..config import settings
from ..filters.admin_filters import IsAdmin
from handlers.utils import UniversalMessageSender, admin_universe_broadcast
from ..keyboards.admin import create_admin_kb, cancel_btn
from ..orm.managers import TeamManager
from ..orm.utils import get_all_users_ids_for_broadcast, get_commander_and_responsible_person, ban_user, \
    get_teams_with_users, get_registration_requests, get_commander
from ..utils.constants import MainKeyboardCommands, AdminKeyboardCommands

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(F.text == MainKeyboardCommands.ADMIN)
async def admin_handler(message: Message):
    await message.answer('Открыт доступ в админку! Выберите действие👇', reply_markup=create_admin_kb())


class Form(StatesGroup):
    all_broadcast_to_bot = State()
    commander_broadcast = State()
    responsible_broadcast = State()
    discussion_with_comment = State()
    discussion_without_comment = State()


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.USERS)
async def cmd_users(call: CallbackQuery, state: FSMContext):
    teams = await get_teams_with_users()
    message = ''
    for team in teams:
        message += f'{team.name}:\n'
        for i, user in enumerate(team.telegram_users, start=1):
            message += f' {i}. {user.callsign} @{user.telegram_username}\n'
        message += '\n'

    await call.message.answer(f'Список пользователей:\n {message}')


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.REGISTRATION_REQUESTS)
async def cmd_users(call: CallbackQuery, state: FSMContext):
    users = await get_registration_requests()

    msg = ''
    count = 0
    for index, user in enumerate(users, start=1):
        user_team = await TeamManager.get_by_id(user.team_id)
        msg += f'{index}.\n'
        msg += f'команда: {user_team}\n'
        msg += f'командир: {"Да" if user.is_commander else "Нет"},\n'
        msg += f'помощник командира: {"Да" if user.responsible_person else "Нет"},\n'
        msg += f'телеграм логин: @{user.telegram_username},\n'
        msg += f'позывной: {user.callsign},\n'
        msg += '\n'
        count += 1
    message = f'Всего заявок: {count}\n\n{msg}'
    await call.message.answer(f'Заявки на регистрацию:\n{message}')


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.ALL_BROADCAST_TO_BOT)
async def admin_all_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем пользователям с базы данных',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.all_broadcast_to_bot)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.all_broadcast_to_bot, IsAdmin())
async def all_broadcast(message: Message, state: FSMContext):
    users_ids = await get_all_users_ids_for_broadcast(message.from_user.id)
    await admin_universe_broadcast(message, state, users_ids)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.COMMANDER_BROADCAST)
async def admin_commander_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем командирам',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.commander_broadcast)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.commander_broadcast)
async def commander_broadcast(message: Message, state: FSMContext):
    users = await get_commander(message.from_user.id)
    users_ids = [user.telegram_id for user in users]
    await admin_universe_broadcast(message, state, users_ids)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.RESPONSIBLE_BROADCAST)
async def admin_commander_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем командирам и ответственным',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.responsible_broadcast)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.responsible_broadcast)
async def responsible_broadcast(message: Message, state: FSMContext):
    users = await get_commander_and_responsible_person(message.from_user.id)
    users_ids = [user.telegram_id for user in users]
    await admin_universe_broadcast(message, state, users_ids)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.CHANNEL_MESSAGE_WITH_COMMENT)
async def admin_commander_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и создам пост с комментариями в канале',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.discussion_with_comment)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.discussion_with_comment)
async def channel_message_with_comment(message: Message, state: FSMContext):
    sender = UniversalMessageSender.init_from_message(message)
    await sender.message_with_discussion(settings.CHAT_ID)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.CHANNEL_MESSAGE_WITHOUT_COMMENT)
async def admin_commander_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и создам пост без комментариев в канале',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.discussion_without_comment)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.discussion_without_comment)
async def channel_message_with_comment(message: Message, state: FSMContext):
    sender = UniversalMessageSender.init_from_message(message)
    await sender.message_without_discussion(settings.CHAT_ID, settings.GROUP_ID)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.CANSEL)
async def cansel_broadcast(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Рассылка отменена!', reply_markup=create_admin_kb())
