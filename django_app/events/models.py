from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Games(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=250,
    )
    descriptions = models.CharField(
        verbose_name='Описание',
        max_length=1000,
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала',
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания',
    )
    organizers = models.CharField(
        verbose_name='Организаторы',
        max_length=250,
    )
    big = models.BooleanField(
        verbose_name='Большая игра',
        default=False,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=50,
    )
    game_area = models.CharField(
        verbose_name='Полигон',
        max_length=50,
    )
    side_commander = models.CharField(
        verbose_name='Командующий стороны',
        max_length=50,
        blank=True,
        null=True,
    )
    judas_commander = models.CharField(
        verbose_name='Командующий Иудой',
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name


class EventChoices(models.IntegerChoices):
    TRAINING = 1, 'Тренировка'
    GATHERING = 2, 'Сбор'


class Event(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=250,
    )
    event_type = models.SmallIntegerField(
        verbose_name='Тип события',
        choices=EventChoices.choices,
    )
    descriptions = models.CharField(
        verbose_name='Описание',
        max_length=1500,
    )
    location = models.CharField(
        verbose_name='Место проведения',
        max_length=250,
    )
    organizers = models.CharField(
        verbose_name='Организаторы',
        max_length=250,
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала',
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания',
    )

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.name


class PeriodChoices(models.IntegerChoices):
    HOURS = 1, 'Час'
    DAYS = 2, 'День'
    WEEK = 3, 'Неделя'
    MONTH = 4, 'Месяц'


class NotificationPeriod(models.Model):
    period = models.SmallIntegerField(
        verbose_name='Период',
        choices=PeriodChoices.choices,
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Период уведомления'
        verbose_name_plural = 'Период уведомлений'

    def __str__(self):
        return f'{self.get_period_display()}/{self.amount}'


class GameEventNotification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    notification_period = models.ForeignKey(
        verbose_name='Период уведомления',
        to=NotificationPeriod,
        on_delete=models.CASCADE,
        related_name='schedulers',
    )
    notified = models.BooleanField(
        verbose_name='Уведомление отправлено',
        default=False,
    )
    notification_date = models.DateTimeField(
        verbose_name='Дата уведомления',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Расписание уведомления'
        verbose_name_plural = 'Расписание уведомлений'

    def __str__(self):
        return f''