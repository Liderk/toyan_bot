from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import Textarea

from events.models import Games, Event, NotificationPeriod, GameEventNotification

from utils.common import get_full_image_link


class GameEventNotificationSchedulerInline(GenericTabularInline):
    model = GameEventNotification
    extra = 0
    readonly_fields = ('notification_date', 'notified')


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'start_date', 'end_date', 'big',
                    'city', 'game_area', 'side_commander', 'toyan_commander')
    readonly_fields = ('game_map_preview', 'location_map_preview')

    inlines = (GameEventNotificationSchedulerInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'descriptions':
            kwargs['widget'] = Textarea()
        return super().formfield_for_dbfield(db_field, **kwargs)

    def game_map_preview(self, obj):
        if not obj.game_map:
            return '-'
        return get_full_image_link(obj.game_map.url)

    game_map_preview.short_description = 'Превью карты'

    def location_map_preview(self, obj):
        if not obj.location_map:
            return '-'
        return get_full_image_link(obj.location_map.url)

    location_map_preview.short_description = 'Превью схемы проезда'


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'descriptions', 'location', 'organizers', 'start_date', 'end_date')
    readonly_fields = ('location_map_preview',)
    inlines = (GameEventNotificationSchedulerInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'descriptions':
            kwargs['widget'] = Textarea()
        return super().formfield_for_dbfield(db_field, **kwargs)

    def location_map_preview(self, obj):
        if not obj.location_map:
            return '-'
        return get_full_image_link(obj.location_map.url)

    location_map_preview.short_description = 'Превью схемы проезда/карты'


@admin.register(NotificationPeriod)
class NotificationSchedulerAdmin(admin.ModelAdmin):
    list_display = ('period', 'amount')
