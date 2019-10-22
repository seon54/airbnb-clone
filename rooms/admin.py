from django.contrib import admin
from django.utils.html import mark_safe
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class RoomTimeAdmin(admin.ModelAdmin):
    """Item Admin Definition"""
    list_display = ('name', 'used_by')

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""
    inlines = (PhotoInline, )
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")}
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
    raw_id_fields = ("host",)
    list_display = (
        'name', 'country', 'city', 'price', 'guest', 'beds', 'bedrooms', 'baths', 'check_in', 'check_out',
        'instant_book', 'count_amenities', 'count_photos', 'total_rating')
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

    list_display = ('__str__', 'get_thumbnail',)

    def get_thumbnail(self, obj):
        return mark_safe(f'<image src="{obj.file.url}" width="50px"/>')

    get_thumbnail.short_description = 'Thumbnail'
