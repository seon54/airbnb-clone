from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from rooms.models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    return render(request, 'rooms/home.html', context={'rooms': rooms})
