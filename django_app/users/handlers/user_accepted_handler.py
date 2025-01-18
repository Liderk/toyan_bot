
from utils.mixins.signal_mixin import SignalMixin

from users.models import TelegramUser
from users.signals.custom_signals import telegram_user_accepted


class UserAcceptedHandler(SignalMixin):
    signal = telegram_user_accepted
    signal_sender = TelegramUser

    def __init__(self, form, instance):
        self.form = form
        self.instance = instance

    def run(self):
        if 'is_active' in self.form.changed_data and self.form.cleaned_data['is_active']:
            self._send_signal(instance=self.instance)
