from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(
        verbose_name='Название команды',
        max_length=64,
        unique=True,
    )
    recruit = models.BooleanField(
        verbose_name='Является рекрутом',
        default=True,
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class TelegramUser(models.Model):
    team = models.ForeignKey(
        to=Team,
        verbose_name='Команда',
        related_name='users',
        on_delete=models.SET_NULL,
        null=True,
    )
    is_commander = models.BooleanField(
        verbose_name='Является командиром',
        default=False,
    )
    responsible_person = models.BooleanField(
        verbose_name='Является ответственным лицом',
        default=False,
    )
    telegram_id = models.PositiveBigIntegerField(
        verbose_name='Телеграм id',
    )
    telegram_username = models.CharField(
        verbose_name='Телеграм логин',
        max_length=256,
    )
    is_active = models.BooleanField(
        verbose_name='Активный пользователь',
        default=False,
        help_text='Если установлен, то пользователь имеет доступа к боту',
    )
    is_admin = models.BooleanField(
        verbose_name='Является ли админом',
        default=False,
        help_text='Если установлен, то пользователь админ бота',
    )
    date_joined = models.DateTimeField(
        'Дата подключения',
        default=timezone.now
    )
    callsign = models.CharField(
        verbose_name='Позывной',
        max_length=256,
    )
    is_banned = models.BooleanField(
        verbose_name='Забанен',
        default=False,
        help_text='Если установлен, то пользователь забанен в боте и канале. '
                  'Ему не будет доступна рассылка и функционал',
    )

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'

    def __str__(self):
        return f'{self.telegram_username}/{self.callsign}'


class User(AbstractUser):
    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return self.username
