from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import (
    AdminUserCreationForm,
    AdminUserChangeForm
)


User = get_user_model()


def ban_users(modeladmin, news, queryset):
    queryset.update(is_banned=True)
ban_users.short_description = "Ban selected Users"


class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ['username', 'email', 'date_joined', 'last_login', 'is_banned', 'is_admin']
    list_filter = ['last_login', 'date_joined', 'is_banned', 'is_admin']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_banned','is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ['username', 'email']
    actions = [ban_users]
    ordering = ['username']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)