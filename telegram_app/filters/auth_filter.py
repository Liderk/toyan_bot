from aiogram.filters import BaseFilter
from aiogram.types import Message

from telegram_app.orm.utils import find_user_by_telegram_id


class AuthFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user = await find_user_by_telegram_id(user_id)
        if user and user.is_active:
            return True
        if user and not user.is_active:
            await message.answer('Заявка на регистрацию на рассмотрении. Ожидайте!', show_alert=True)

        if user is None:
            await message.answer('Для доступа к боту необходимо зарегистрироваться.\n\n'
                                 'Выполни команду <b>/register</b> и следуй инструкциям!\n\n'
                                 'Регистрация обрабатывается в ручную. '
                                 'Когда отцы командиры одобрят твою кандидатуру, ты будешь уведомлен!', show_alert=True)

        return False