from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from events.models import Games, Event, NotificationPeriod, GameEventNotification


class GameEventNotificationSchedulerInline(GenericTabularInline):
    model = GameEventNotification
    extra = 0


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'start_date', 'end_date', 'big',
                    'city', 'game_area', 'side_commander', 'judas_commander')

    inlines = (GameEventNotificationSchedulerInline,)


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'descriptions', 'location', 'organizers', 'start_date', 'end_date')
    inlines = (GameEventNotificationSchedulerInline,)


@admin.register(NotificationPeriod)
class NotificationSchedulerAdmin(admin.ModelAdmin):
    list_display = ('period', 'amount')
