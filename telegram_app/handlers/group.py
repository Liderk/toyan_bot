from aiogram import Router
from aiogram.types import Message

from config import settings
from filters.access_group import AccessGroupFilter
from filters.delete_group_message import DeleteGroupMessage
from handlers.utils import InMemoryMessageIdStorage
from init_bot import bot

group_router = Router()
group_router.message.filter(
    AccessGroupFilter(chat_type=["group", "supergroup"], allowed_group_chats=[settings.GROUP_ID]),
)


@group_router.message(DeleteGroupMessage())
async def delete_discussion_message(message: Message):
    await bot.delete_message(chat_id=settings.GROUP_ID, message_id=message.message_id)
    InMemoryMessageIdStorage.delete_msg(message.forward_from_message_id)

