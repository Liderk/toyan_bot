from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import Textarea

from events.models import Games, Event, NotificationPeriod, GameEventNotification


class GameEventNotificationSchedulerInline(GenericTabularInline):
    model = GameEventNotification
    extra = 0
    readonly_fields = ('notification_date',)


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'start_date', 'end_date', 'big',
                    'city', 'game_area', 'side_commander', 'judas_commander')

    inlines = (GameEventNotificationSchedulerInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'descriptions':
            kwargs['widget'] = Textarea()
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'descriptions', 'location', 'organizers', 'start_date', 'end_date')
    inlines = (GameEventNotificationSchedulerInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'descriptions':
            kwargs['widget'] = Textarea()
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(NotificationPeriod)
class NotificationSchedulerAdmin(admin.ModelAdmin):
    list_display = ('period', 'amount')
