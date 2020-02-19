from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django.utils import timezone
from core.models import TimeStampedModel
from cal import Calendar


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
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="photos")

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
    check_in = models.DateField()
    check_out = models.DateField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )
    room_type = models.ForeignKey(
        "RoomType", on_delete=models.SET_NULL, null=True, related_name="rooms"
    )
    amenities = models.ManyToManyField("Amenity", blank=True, related_name="rooms")
    facilities = models.ManyToManyField("Facility", blank=True, related_name="rooms")
    rules = models.ManyToManyField("HouseRule", blank=True, related_name="rooms")

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            photo = self.photos.first()
            return photo.file.url
        except Exception:
            return None

    def get_next_four(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def get_beds(self):
        return "1 bed" if self.beds == 1 else f'{self.beds} beds'

    def get_calendars(self):
        year = timezone.now().year
        month = timezone.now().month
        next_month = month + 1
        if month == 12:
            next_month = 1
        this_month_cal = Calendar(year, month)
        next_month_cal = Calendar(year, next_month)
        return [this_month_cal, next_month_cal]

    def save(self, *args, **kwargs):
        self.city = str.title(self.city)
        super().save(*args, **kwargs)
