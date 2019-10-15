from django.utils import timezone
from django.db import models
from core.models import TimeStampedModel


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

    def __str__(self):
        return f'{self.room}: {self.check_in}'

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in < now < self.check_out

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    in_progress.boolean = True
    is_finished.boolean = True


