from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from rooms.models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10)
    try:
        rooms = paginator.page(int(page))
        return render(request, 'rooms/home.html', context={'rooms': rooms})
    except EmptyPage:
        return redirect('/')
