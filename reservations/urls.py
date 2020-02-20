from django.urls import path

from reservations import views

app_name = "reservations"

urlpatterns = [
    path("create/<int:room>/<int:year>-<int:month>-<int:day>", views.create, name="create"),
    path("<int:pk>", views.ReservationDetailView.as_view(), name="detail"),
]
