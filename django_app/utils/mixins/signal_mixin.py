import types

from django.db import transaction


class SignalMixin:
    """Примесь, добавляющая возможность отправки сигнала. Отравляет сигнал после завершения транзакции."""

    _signal_prevented: bool = False
    signal = None
    signal_sender = None

    def prevent_signal_send(self) -> None:
        """
        Метод предотвращения отправки сигнала.

        Удобно, когда один обработчик вызывается внутри другого, и есть
        необходимость не отправлять сигнал

        """
        self._signal_prevented = True

    def _send_signal(self, **kwargs) -> None:
        """Основной метод отправки сигнала."""
        if self._signal_prevented:
            return

        self._inner_send_signal(**kwargs)

    @classmethod
    def _inner_send_signal(cls, **kwargs) -> None:
        signal_kwargs = cls._get_signal_kwargs(**kwargs)

        if isinstance(signal_kwargs, types.GeneratorType):
            """
            Метод подготовки данных для сигнала вернул генератор - бежим по генератору и отправляем много сигналов
            с параметрами, которые возвращает генератор.

            """
            for kwargs_ in signal_kwargs:
                cls.send_signal(**kwargs_)

        else:
            cls.send_signal(**signal_kwargs)

    @staticmethod
    def _get_signal_kwargs(**kwargs) -> dict:
        """Метод подготовки параметров для сигнала. Иногда удобно."""
        return kwargs

    @classmethod
    def send_signal(cls, **kwargs) -> None:
        """Отправка сигнала. Устанавливает задачу как callback применения транзакции."""

        def send() -> None:
            cls.signal.send(sender=cls.signal_sender, **kwargs)

        transaction.on_commit(send)
