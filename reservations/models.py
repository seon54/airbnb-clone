import datetime

from django.utils import timezone
from django.db import models
from core.models import TimeStampedModel
from reservations.managers import CustomReservationManager


class Reservation(TimeStampedModel):
    """Reservation Model Definition"""
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELED, 'Canceled'),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()

    objects = CustomReservationManager()

    def __str__(self):
        return f'{self.room}: {self.check_in}'

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in <= now < self.check_out

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    def save(self, *args, **kwargs):
        start = self.check_in
        end = self.check_out
        difference = end - start
        existing_booked_day = BookedDay.objects.filter(day__range=(start, end), reservation__room=self.room).exists()
        if not existing_booked_day:
            super().save(*args, **kwargs)
            for i in range(difference.days + 1):
                day = start + datetime.timedelta(days=i)
                BookedDay.objects.get_or_create(day=day, reservation=self)
        else:
            return super().save(*args, **kwargs)

    in_progress.boolean = True
    is_finished.boolean = True


class BookedDay(TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='booked')

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)
