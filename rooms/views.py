from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django_countries import countries

from rooms.forms import SearchForm, CreatePhotoForm, CreateRoomForm
from rooms.models import Room, Photo
from users.mixins import LoggedInOnlyView


class HomeView(ListView):
    """ Home View Definition """

    model = Room
    paginate_by = 12
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ Room Detail Definition"""

    model = Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get('country')
        if countries:
            form = SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                superhost = form.cleaned_data.get('superhost')
                amenities = form.cleaned_data.get('amenities')
                facilities = form.cleaned_data.get('facilities')

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guest__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = Room.objects.filter(**filter_args).order_by('-created')
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get('page', 1)
                rooms = paginator.get_page(page)

                return render(request, "rooms/search.html", {'form': form, 'rooms': rooms})
        else:
            form = SearchForm()
        return render(request, "rooms/search.html", {'form': form})


class EditRoomView(LoggedInOnlyView, UpdateView):
    model = Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guest",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "rules",
    )
    template_name = 'rooms/room_edit.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(LoggedInOnlyView, DetailView):
    model = Room
    template_name = 'rooms/room_photos.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete this photo")
        else:
            Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except Room.DoesNotExist:
        return request(reverse("core:home"))


class EditPhotoView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = 'rooms/edit_photo.html'
    fields = ("caption",)
    pk_url_kwarg = 'photo_pk'
    success_message = 'Photo Updated'

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(LoggedInOnlyView, FormView):
    template_name = 'rooms/photo_create.html'
    fields = ('caption', 'file',)
    form_class = CreatePhotoForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse('rooms:photos', kwargs={'pk': pk}))

    def form_invalid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        messages.error(self.request, "Upload failed")
        return redirect(reverse('rooms:photos', kwargs={'pk': pk}))


class CreateRoomView(LoggedInOnlyView, FormView):
    form_class = CreateRoomForm
    template_name = 'rooms/room_create.html'

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, 'Room uploaded')
        return redirect(reverse('rooms:detail', kwargs={'pk': room.pk}))
