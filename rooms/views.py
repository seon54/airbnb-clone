from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.urls import reverse
from django_countries import countries
from rooms.models import Room, RoomType


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
    room_types = RoomType.objects.all()

    form = {
        "city": city, "s_room_type": room_type, "s_country": country
    }

    choices = {
        "countries": countries, "room_types": room_types
    }
    return render(request, "rooms/search.html", {**form, **choices})
