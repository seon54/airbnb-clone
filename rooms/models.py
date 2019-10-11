from django.db import models
from django_countries.fields import CountryField
from core.models import TimeStampedModel
from users.models import User


class AbstractItem(TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class RoomType(AbstractItem):
    pass


class Room(TimeStampedModel):
    """ Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guest = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ManyToManyField(RoomType, blank=True)

    def __str__(self):
        return self.name
