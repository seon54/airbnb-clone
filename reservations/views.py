import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from reservations.models import BookedDay, Reservation
from rooms.models import Room


class CreationError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = Room.objects.get(pk=room)
        BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreationError()
    except Room.DoesNotExist:
        messages.error(request, "Can't Reserve That Room.")
        return redirect(reverse("core:home"))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create(guest=request.user, room=room, check_in=date_obj,
                                                 check_out=date_obj + datetime.timedelta(days=1))
        return redirect(reverse("reservations:detail", kwargs={'pk': reservation.pk}))


class ReservationDetailView(View):

    def get(self, request, pk):
        reservation = Reservation.objects.get_or_none(pk=pk)
        print(reservation)
        if not reservation or (reservation.guest != request.user and reservation.room.host != request.user):
            raise Http404()
        return render(request, "reservations/detail.html", {"reservation": reservation})
