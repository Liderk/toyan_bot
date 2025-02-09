from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from telegram_app.config import settings
from telegram_app.filters.admin_filters import IsAdmin
from telegram_app.handlers.utils import UniversalMessageSender, universe_broadcast
from telegram_app.keyboards.admin import create_admin_kb, cancel_btn
from telegram_app.orm.utils import get_all_users_ids_for_broadcast, get_commander_users_ids_for_broadcast
from telegram_app.utils.constants import MainKeyboardCommands, AdminKeyboardCommands

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(F.text == MainKeyboardCommands.ADMIN)
async def admin_handler(message: Message):
    await message.answer('Открыт доступ в админку! Выберите действие👇', reply_markup=create_admin_kb())


class Form(StatesGroup):
    all_broadcast_to_bot = State()
    commander_broadcast = State()
    discussion_with_comment = State()
    discussion_without_comment = State()


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
    await universe_broadcast(message, state, users_ids)


# __________________________________________________________________________________
@admin_router.callback_query(F.data == AdminKeyboardCommands.COMMANDER_BROADCAST)
async def admin_commander_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем командирам и ответственным',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.commander_broadcast)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.commander_broadcast)
async def commander_broadcast(message: Message, state: FSMContext):
    users_ids = await get_commander_users_ids_for_broadcast(message.from_user.id)
    await universe_broadcast(message, state, users_ids)


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
