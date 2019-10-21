from django.db import models

from core.models import TimeStampedModel


class Review(TimeStampedModel):
    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.review} - {self.room}'

    def rating_average(self):
        avg = (self.accuracy + self.communication + self.cleanliness + self.location + self.check_in + self.value) / 6
        return round(avg)
    rating_average.short_description = 'Avg.'
