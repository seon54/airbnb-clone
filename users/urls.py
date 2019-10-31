from django.urls import path
from .views import LoginView, logout_view, SignUpView

app_name='users'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
]