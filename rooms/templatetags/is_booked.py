import datetime

from django import template

from reservations.models import BookedDay

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return ""
    try:
        day = datetime.datetime(year=day.year, month=day.month, day=day.number)
        BookedDay.objects.get(day=day, reservation__room=room)
        return True
    except BookedDay.DoesNotExist:
        return False


