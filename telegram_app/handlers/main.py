from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from filters.auth_filter import AuthFilter
from handlers.utils import simple_universe_broadcast
from init_bot import bot
from keyboards.admin import cancel_btn
from keyboards.main_text_kb import create_main_text_kb
from orm.utils import get_admin_ids
from utils.constants import Commands, MainKeyboardCommands

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    keyboard = await create_main_text_kb(message.from_user.id)
    await message.answer('Добро пожаловать! Доступ только для участников ТГ Тоян', reply_markup=keyboard)


@main_router.message(Command(Commands.MENU))
async def main_keyboard(message: Message):
    keyboard = await create_main_text_kb(message.from_user.id)
    if not message.from_user.is_bot:
        await message.answer('Вот тебе клавиатура', reply_markup=keyboard)


@main_router.message(F.text == MainKeyboardCommands.ABOUT)
async def about(message: Message):
    msg = ('<i>Я — кара Господня. Если вы не совершали смертельных грехов, '
           'Господь не пошлёт вам кару в лице меня!</i> \n\n'
           '<b>Оповещения</b>: Оповещения о предстоящих играх и других событиях ТГ Тоян\n\n'
           '<b>Уведомления</b>: Разнообразные уведомления отцов командиров\n\n'
           '<b>Информация</b>: Самостоятельно запрашивать информацию о предстоящих мероприятиях\n\n')
    await message.answer(msg)


class Form(StatesGroup):
    admin_q = State()


@main_router.message(F.text == MainKeyboardCommands.ADMIN_Q, AuthFilter())
async def question_for_admin(message: Message, state: FSMContext):
    await message.answer(
        'Напиши любое сообщение, я передам его админам',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.admin_q)


@main_router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'voice'}),
                     Form.admin_q)
async def question_for_admin_broadcast(message: Message, state: FSMContext):
    admin_ids = await get_admin_ids()
    username = message.from_user.username or f'{message.from_user.full_name}'
    for admin_id in admin_ids:
        msg = f'Тут какой то поц @{username}, хочет задать вопрос админам:'
        await bot.send_message(chat_id=admin_id, text=msg)
    await simple_universe_broadcast(message, admin_ids)
    await state.clear()
