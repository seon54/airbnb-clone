from django.contrib import admin

from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class RoomTimeAdmin(admin.ModelAdmin):
    """Item Admin Definition"""
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""
    pass
