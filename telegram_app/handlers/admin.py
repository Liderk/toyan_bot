from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from telegram_app.filters.admin_filters import IsAdmin
from telegram_app.handlers.utils import broadcast_message
from telegram_app.keyboards.admin import create_admin_kb, cancel_btn
from telegram_app.orm.utils import get_all_users_ids_for_broadcast, get_commander_users_ids_for_broadcast
from telegram_app.utils.constants import MainKeyboardCommands, AdminKeyboardCommands

admin_router = Router()


@admin_router.message(F.text == MainKeyboardCommands.ADMIN, IsAdmin())
async def admin_handler(message: Message):
    await message.answer('Открыт доступ в админку! Выберите действие👇', reply_markup=create_admin_kb())


class Form(StatesGroup):
    all_broadcast = State()
    commander_broadcast = State()


@admin_router.callback_query(F.data == AdminKeyboardCommands.ALL_BROADCAST, IsAdmin())
async def admin_all_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем пользователям с базы данных',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.all_broadcast)


@admin_router.callback_query(F.data == AdminKeyboardCommands.COMMANDER_BROADCAST, IsAdmin())
async def admin_all_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправь любое сообщение, а я его перехвачу и перешлю всем пользователям с базы данных',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.commander_broadcast)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.all_broadcast, IsAdmin())
async def all_broadcast(message: Message, state: FSMContext):
    users_ids = await get_all_users_ids_for_broadcast(message.from_user.id)
    await universe_broadcast(message, state, users_ids)


@admin_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                      Form.commander_broadcast, IsAdmin())
async def commander_broadcast(message: Message, state: FSMContext):
    users_ids = await get_commander_users_ids_for_broadcast(message.from_user.id)
    await universe_broadcast(message, state, users_ids)


async def universe_broadcast(message: Message, state: FSMContext, user_ids: list[int]):
    content_type = message.content_type

    await message.answer(f'Начинаю рассылку на {len(user_ids)} пользователей.')

    good_send, bad_send = await broadcast_message(
        users_ids=user_ids,
        text=message.text if content_type == ContentType.TEXT else None,
        photo_id=message.photo[-1].file_id if content_type == ContentType.PHOTO else None,
        document_id=message.document.file_id if content_type == ContentType.DOCUMENT else None,
        video_id=message.video.file_id if content_type == ContentType.VIDEO else None,
        audio_id=message.audio.file_id if content_type == ContentType.AUDIO else None,
        voice_id=message.voice.file_id if content_type == ContentType.VOICE else None,
        caption=message.caption,
        content_type=content_type,
    )

    await state.clear()
    await message.answer(f'Рассылка завершена. Сообщение получило <b>{good_send}</b>, '
                         f'НЕ получило <b>{bad_send}</b> пользователей.', reply_markup=create_admin_kb())


@admin_router.callback_query(F.data == AdminKeyboardCommands.CANSEL, IsAdmin())
async def cansel_broadcast(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Рассылка отменена!', reply_markup=create_admin_kb())
