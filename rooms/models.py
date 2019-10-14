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
    """ Room Type Definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):
    """Amenity Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """House Rule Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(TimeStampedModel):
    """Photo Model Definition"""
    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


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
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    rules = models.ManyToManyField("HouseRule", blank=True)

    def __str__(self):
        return self.name
