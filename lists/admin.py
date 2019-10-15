from django.contrib import admin
from .models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    """List Admin Definition"""
    list_display = ('name', 'user', 'count_rooms')
    search_fields = ('name',)
    filter_horizontal = ('rooms',)
