from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'role', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Rôle', {'fields': ('role',)}),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
