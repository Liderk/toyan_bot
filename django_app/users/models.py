from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    team = models.CharField(
        verbose_name='Название команды',
        max_length=100,
        blank=True,
        null=True,
    )
    is_commander = models.BooleanField(
        verbose_name='Является командиром',
        default=False,
    )
    telegram_id = models.PositiveBigIntegerField(
        verbose_name='Телеграм id',
        blank=True,
        null=True,
    )
    password = models.CharField(
        verbose_name=_("password"),
        max_length=128,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тояновец'
        verbose_name_plural = 'Тояновцы'

    def __str__(self):
        return self.username
