from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_app.keyboards.main_text_kb import create_main_text_kb
from telegram_app.utils.constants import Commands, MainKeyboardCommands

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    keyboard = await create_main_text_kb(message.from_user.id)
    await message.answer('Добро пожаловать! Доступ только для участников ТГ Тоян', reply_markup=keyboard)


@main_router.message(Command(Commands.MAIN_KEYBOARD))
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
