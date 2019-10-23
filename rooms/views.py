from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from rooms.models import Room


class HomeView(ListView):
    """ Home View Definition """

    model = Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except Room.DoesNotExist:
        raise Http404()

