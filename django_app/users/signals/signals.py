import asyncio
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db.models import Model
from django.dispatch import receiver

from users.models import TelegramUser
from users.signals.custom_signals import telegram_user_accepted
from utils.telegram_bot import bot


@receiver(signal=telegram_user_accepted, sender=TelegramUser)
def user_accepted(sender: Model, instance: TelegramUser, **kwargs):
    asyncio.run(async_user_accepted(instance))


async def async_user_accepted(instance):
    link_expired = 1
    msg = (f'Кандидатура одобрена, получен доступ до бота\n\n'
           'Так же открылся доступ в группу Тоян: {chat_link}\n'
           'Ссылка действительна в течении 1 суток.')
    expire_date = datetime.now(tz=pytz.timezone('Asia/Novosibirsk')) + timedelta(days=link_expired)
    chat_invite_link = await bot.create_chat_invite_link(chat_id=settings.CHAT_ID,
                                                         expire_date=expire_date, member_limit=1)
    msg = msg.format(chat_link=chat_invite_link.invite_link, days=link_expired)

    await bot.send_message(chat_id=instance.telegram_id, text=msg)
