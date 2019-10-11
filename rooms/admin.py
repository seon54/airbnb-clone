from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Room


@admin.register(Room)
class RoomAdmin(UserAdmin):
    pass
