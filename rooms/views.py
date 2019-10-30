from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.urls import reverse
from django_countries import countries
from rooms.models import Room, RoomType, Amenity, Facility


class HomeView(ListView):
    """ Home View Definition """

    model = Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ Room Detail Definition"""

    model = Room


def search(request):
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city, "s_room_type": room_type, "s_country": country, "price": price, "guests": guests,
        "bedrooms": bedrooms, "beds": beds, "baths": baths, "s_amenities": s_amenities, "s_facilities": s_facilities,
        "instant": instant, "superhost": superhost
    }

    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()

    choices = {
        "countries": countries, "room_types": room_types,
        "amenities": amenities, "facilities": facilities
    }
    filter_args = {}
    if city != 'Anywhere':
        filter_args["city__startswith"] = city

    if room_type != 0:
        filter_args['room_type__pk'] = room_type

    if price != 0:
        filter_args['price__lte'] = price

    if guests != 0:
        filter_args['guest__gte'] = guests

    if bedrooms != 0:
        filter_args['bedrooms__gte'] = bedrooms

    if beds != 0:
        filter_args['beds__gte'] = beds

    if baths != 0:
        filter_args['baths__gte'] = baths

    if instant:
        filter_args['instant_book'] = True

    if superhost:
        filter_args['host__superhost'] = True

    filter_args["country"] = country

    if s_amenities:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if s_facilities:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, 'rooms': rooms})
