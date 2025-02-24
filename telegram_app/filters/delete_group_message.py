from aiogram.filters import BaseFilter
from aiogram.types import Message

from ..handlers.utils import InMemoryMessageIdStorage
from ..utils.constants import MsgAction


class DeleteGroupMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        msg_action = InMemoryMessageIdStorage.check_msg(message.forward_from_message_id)
        return msg_action and msg_action == MsgAction.delete
