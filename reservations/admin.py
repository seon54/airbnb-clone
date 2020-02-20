from django.contrib import admin
from .models import Reservation, BookedDay


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""
    list_display = ('id', 'room', 'status', 'check_in', 'check_out', 'guest', 'in_progress', 'is_finished')
    list_display_links = ('id', 'room', 'status', 'check_in', 'check_out', 'guest', 'in_progress', 'is_finished')
    list_filter = ('status',)


@admin.register(BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'reservation')
    list_display_links = ('day', )
