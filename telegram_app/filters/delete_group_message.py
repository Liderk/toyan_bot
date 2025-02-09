from aiogram.filters import BaseFilter
from aiogram.types import Message

from telegram_app.handlers.utils import InMemoryMessageIdStorage
from telegram_app.utils.constants import MsgAction


class DeleteGroupMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        msg_action = InMemoryMessageIdStorage.check_msg(message.forward_from_message_id)
        return msg_action and msg_action == MsgAction.delete
