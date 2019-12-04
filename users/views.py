import os
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView
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
    messages.info(request, "See you later")
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('core:home')

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


def github_login(request):
    client_id = os.environ.get('GH_ID')
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scoope=read:user')


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get('code', None)
        client_id = os.environ.get('GH_ID')
        client_secret = os.environ.get('GH_SECRET')

        if code is not None:
            result = requests.post(
                f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}',
                headers={"Accept": "application/json"})
            token_json = result.json()
            error = token_json.get('error', None)

            if error is not None:
                raise GithubException("Can't get access token.")
            else:
                access_token = token_json.get('access_token')
                profile_request = requests.get(
                    'https://api.github.com/user',
                    headers={"Authorization": f'token {access_token}', "Accept": "application/json"})
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise GithubException(f'Please login with {user.login_method}.')
                    except User.DoesNotExist:
                        user = User.objects.create(username=email, first_name=name, bio=bio, email=email,
                                                   login_method=User.LOGIN_GITHUB, email_verified=True)
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f'Welcome back {user.first_name}')
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException("Can't get your profile.")
        else:
            raise GithubException("Can't get a code.")
    except GithubException as e:
        messages.error(request, e)
        return reverse(reverse('users:login'))


def kakao_login(request):
    client_id = os.environ.get('KAKAO_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code')


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get('KAKAO_ID')
        code = request.GET.get('code')
        redirect_url = 'http://127.0.0.1:8000/users/login/kakao/callback'
        token_request = requests.post(
            f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_url}&code={code}')
        token_json = token_request.json()
        error = token_json.get('error', None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get('access_token')
        profile_request = requests.get(
            'https://kapi.kakao.com/v2/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        profile_json = profile_request.json()
        kakao_accouant = profile_json.get('kakao_account')
        email = kakao_accouant.get('email')
        if email is None:
            raise KakaoException("Please write your email.")
        profile = kakao_accouant.get('profile')
        nickname = profile.get('nickname')
        profile_image = profile.get('profile_image_url')
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with {user.login_method}.")
        except User.DoesNotExist:
            user = User.objects.create(email=email, first_name=nickname, login_method=User.LOGIN_KAKAO,
                                       email_verified=True, username=nickname)
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f'{nickname}-avatar', ContentFile(photo_request.content))
        login(request, user)
        messages.success(request, f'Welcome back {user.first_name}')
        return redirect(reverse('core:home'))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user_obj'


class UpdateProfileView(UpdateView):
    model = User
