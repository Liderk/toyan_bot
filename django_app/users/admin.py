from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import admin as auth_admin

from users.handlers.user_accepted_handler import UserAcceptedHandler
from users.forms import UserAdminChangeForm, UserAdminCreationForm

from users.models import Team, TelegramUser

User = get_user_model()


@admin.register(User)
class UsersAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    search_fields = ('username',)
    search_help_text = _('Имя пользователя')
    list_filter = ('is_superuser', 'is_active')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'telegram_id', 'team', 'is_commander', 'responsible_person',
                    'is_active', 'is_admin', 'date_joined')
    search_fields = ('team', 'is_commander', 'responsible_person', 'is_admin', 'is_active')

    def save_model(self, request, obj, form, change) -> None:  # noqa: ANN001
        super().save_model(request, obj, form, change)
        if change:
            handler = UserAcceptedHandler(form, obj)
            handler.run()


class TelegramUserInline(admin.TabularInline):
    model = TelegramUser
    extra = 0
    fields = ('telegram_username', 'is_commander', 'responsible_person')


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recruit')
    inlines = (TelegramUserInline,)


admin.site.unregister(Group)
