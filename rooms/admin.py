from django.contrib import admin

from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class RoomTimeAdmin(admin.ModelAdmin):
    """Item Admin Definition"""
    list_display = ('name', 'used_by')

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")}
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")}
        ),
        (
            "Space",
            {"fields": ("guest", "beds", "bedrooms"), }
        ),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "rules"),
             "classes": ("extrapretty", "collapse",)}
        ),
        (
            "Last Detail",
            {"fields": ("host",)}
        )

    )
    list_display = (
        'name', 'country', 'city', 'price', 'guest', 'beds', 'bedrooms', 'baths', 'check_in', 'check_out',
        'instant_book', 'count_amenities', 'count_photos')
    list_filter = (
        'instant_book', 'host__superhost', 'city', 'room_type', 'amenities', 'facilities', 'rules',
        'country',)
    search_fields = ['=city', '^host__username']
    filter_horizontal = ('amenities', 'facilities', 'rules')
    ordering = ('name', 'price',)

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_amenities.short_description = 'amenities'
    count_photos.short_description = 'photos'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""
    pass
