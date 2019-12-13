from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_active', 'language', 'currency', 'superhost',
        'is_staff', 'is_superuser', 'email_verified', 'email_secret', 'login_method')
    list_filter = UserAdmin.list_filter + ('superhost',)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "currency",
                    "language",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )
