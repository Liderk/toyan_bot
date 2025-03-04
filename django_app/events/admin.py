from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import Textarea
from django.utils.html import format_html

from events.models import Games, Event, NotificationPeriod, GameEventNotification


class GameEventNotificationSchedulerInline(GenericTabularInline):
    model = GameEventNotification
    extra = 0
    readonly_fields = ('notification_date', 'notified')


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'start_date', 'end_date', 'big',
                    'city', 'game_area', 'side_commander', 'toyan_commander')
    readonly_fields = ('game_map_preview', 'location_map_preview')
    fields = ('name', 'descriptions', 'start_date', 'end_date', 'organizers',
              'big', 'city', 'game_area', 'side_commander', 'toyan_commander',
              'game_map', 'game_map_preview', 'location_map', 'location_map_preview')

    inlines = (GameEventNotificationSchedulerInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'descriptions':
            kwargs['widget'] = Textarea()
        return super().formfield_for_dbfield(db_field, **kwargs)

    def game_map_preview(self, obj):
        if not obj.game_map:
            return '-'
        return self.get_full_image_link(obj.game_map.url)

    game_map_preview.short_description = 'Превью карты'

    def location_map_preview(self, obj):
        if not obj.location_map:
            return '-'
        return self.get_full_image_link(obj.location_map.url)

    location_map_preview.short_description = 'Превью схемы проезда'

    @staticmethod
    def get_full_image_link(url):
        preview = format_html(f'<img src="{url}" style="max-height: 200px;">')

        return format_html(f'<a href="{url}" target="_blank">{preview}</a>')


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
