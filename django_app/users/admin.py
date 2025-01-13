from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import admin as auth_admin

from users.forms import UserAdminChangeForm, UserAdminCreationForm

from users.models import Team

User = get_user_model()


@admin.register(User)
class UsersAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'team', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'telegram_id', 'telegram_username')}),
        (_('Команда'), {'fields': ('team', 'is_commander', 'responsible_person')}),
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
    list_filter = ('team', 'is_superuser', 'is_active')


class UserTeamInline(admin.TabularInline):
    model = User
    extra = 0
    fields = ('username', 'is_commander', 'telegram_username')


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recruit')
    inlines = (UserTeamInline,)


admin.site.unregister(Group)
