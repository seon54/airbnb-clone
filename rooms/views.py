from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse
from rooms.models import Room


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
