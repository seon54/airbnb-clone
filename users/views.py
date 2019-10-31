from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm, SignUpForm
from .models import User


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('core:home')
    initial = {
        'first_name': 'test2',
        'last_name': 'test2',
        'email': 'test2@email.com',
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        print(user)
        user.save()
    except User.DoesNotExist:
        # TODO: add error message
        pass
    return redirect(reverse("core:home"))
