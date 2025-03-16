from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db.models import Model
from django.dispatch import receiver

from users.models import TelegramUser
from users.signals.custom_signals import telegram_user_accepted
from telegram import Bot


@receiver(signal=telegram_user_accepted, sender=TelegramUser)
def user_accepted(sender: Model, instance: TelegramUser, **kwargs):
    link_expired = 1
    bot = Bot(token=settings.BOT_TOKEN)
    expire_date = datetime.now(tz=pytz.timezone('Asia/Novosibirsk')) + timedelta(days=link_expired)
    invite_link = bot.create_chat_invite_link(
        chat_id=settings.CHAT_ID,
        member_limit=1,  # Ссылка действует на 1 человека
        expire_date=expire_date
    )
    msg = (f'Кандидатура одобрена, получен доступ до бота\n\n'
           'Так же открылся доступ в группу Тоян: {chat_link}\n'
           'Ссылка действительна в течении 1 суток.')
    msg = msg.format(chat_link=invite_link, days=link_expired)
    bot.send_message(chat_id=instance.telegram_id, text=msg)
