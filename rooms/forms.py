from django import forms
from django_countries.fields import CountryField
from rooms.models import RoomType, Amenity, Facility, Photo, Room


class SearchForm(forms.Form):
    city = forms.CharField(initial='Anywhere')
    country = CountryField(default='KR').formfield()
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), empty_label='Any kind', required=False)
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    badrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), widget=forms.CheckboxSelectMultiple,
                                               required=False)
    facilities = forms.ModelMultipleChoiceField(queryset=Facility.objects.all(), widget=forms.CheckboxSelectMultiple,
                                                required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('caption', 'file')

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        photo.room = Room.objects.get(pk=pk)
        photo.save()
