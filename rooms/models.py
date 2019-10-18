from django.db import models
from django_countries.fields import CountryField
from core.models import TimeStampedModel


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
    file = models.ImageField(upload_to='room_photos')
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name='photos')

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
    host = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True, related_name='rooms')
    amenities = models.ManyToManyField("Amenity", blank=True, related_name='rooms')
    facilities = models.ManyToManyField("Facility", blank=True, related_name='rooms')
    rules = models.ManyToManyField("HouseRule", blank=True, related_name='rooms')

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            # TODO: ZeroDivisionError
            all_ratings += review.rating_average()
        return all_ratings / len(all_reviews)

    def save(self, *args, **kwargs):
        self.city = str.title(self.city)
        super().save(*args, **kwargs)