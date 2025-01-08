import logging

from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message, CallbackQuery

from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from telegram_app.orm.utils import find_user_by_telegram_id
from telegram_app.utils.constants import Commands

logger = logging.getLogger(__name__)


class UserCheckMiddleware(BaseMiddleware):

    async def on_process_event(self, message: Message):
        user_id = message.event.from_user.id
        user = await find_user_by_telegram_id(user_id)
        if user and user.is_active:
            return
        if user and not user.is_active:
            raise CancelHandler('Заявка на регистрацию на рассмотрении. Ожидайте!')
        raise CancelHandler('Для доступа к боту необходимо зарегистрироваться.\n\n'
                            'Выполни команду <b>/register</b> и следуй инструкциям!\n\n'
                            'Регистрация обрабатывается в ручную. '
                            'Когда отцы командиры одобрят твою кандидатуру, ты будешь уведомлен!')

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        if isinstance(event.event, CallbackQuery):
            msg = 'check_user_id'
            message_for_answer = event.event.message
        else:
            msg = event.message.text.replace('/', '') if event.message.text else event.message.text
            message_for_answer = event.message

        if msg not in (Commands.REGISTER,):
            try:
                await self.on_process_event(event)
            except CancelHandler as err:
                await message_for_answer.answer(str(err), show_alert=True)
                return

        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(e)

        return
