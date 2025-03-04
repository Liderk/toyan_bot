from aiogram.filters import BaseFilter
from aiogram.types import Message

from orm.utils import get_admin_ids


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        admin_ids = await get_admin_ids()
        return message.from_user.id in admin_ids
