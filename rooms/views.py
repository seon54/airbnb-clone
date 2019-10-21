from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from rooms.models import Room


def all_rooms(request):
    all_rooms = Room.objects.all()
    return render(request, 'rooms/home.html', context={'rooms': all_rooms})
