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
        blank=True,
        null=True,
    )
    telegram_username = models.CharField(
        verbose_name='Телеграм логин',
        max_length=256,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='Активный пользователь',
        default=True,
        help_text='Если установлен, то пользователь имеет доступа к боту',
    )
    models.DateTimeField(_("date joined"), default=timezone.now)


class User(AbstractUser):
    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return self.username
