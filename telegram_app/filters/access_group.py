from aiogram.filters import BaseFilter
from aiogram.types import Message


class AccessGroupFilter(BaseFilter):
    def __init__(self, chat_type: (str, list), allowed_group_chats: list[int]):
        self.chat_type = chat_type
        self.allowed_group_chats = allowed_group_chats

    def is_message_from_group(self, message: Message):
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type

    async def __call__(self, message: Message) -> bool:
        if not self.is_message_from_group(message):
            return True

        if message.chat.id in self.allowed_group_chats:
            return True
        return False
