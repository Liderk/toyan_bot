import asyncio

from django.db.models import Model
from django.dispatch import receiver


from users.models import TelegramUser
from telegram_app.init_bot import bot
from users.signals.custom_signals import telegram_user_accepted

print('#' * 100)


@receiver(signal=telegram_user_accepted, sender=TelegramUser)
def user_acccepted(sender: Model, instance: TelegramUser, **kwargs):
    msg = 'Кандидатура одобрена, получен доступ до бота'
    asyncio.run(bot.send_message(chat_id=instance.telegram_id, text=msg))

