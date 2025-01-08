from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import admin as auth_admin

from users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UsersAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'team', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'telegram_id')}),
        (_('Команда'), {'fields': ('team', 'is_commander')}),
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


admin.site.unregister(Group)
