from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .serializers import UserSerializer, LoginSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .forms import RegisterUserForm
from django.shortcuts import render
from django.utils import timezone


@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            redirect_url = request.GET.get('next', '/')
            subject = 'Регистрация успешна'
            html_message = render_to_string('email_templates/registration_confirmation.html', {'user': user})
            plain_message = strip_tags(html_message)
            from_email = 'noreply.onlinecourses@gmail.com'
            to_email = user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            # Авторизация пользователя
            auth_user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
            if auth_user:
                login(request, auth_user)
                return redirect(redirect_url)
        else:
            # Если форма неверна, поля не будут опустошаться
            error_message = 'Некорректные данные при регистрации'
            return render(request, 'registration.html', {'form': form, 'error_message': error_message})
    else:
        form = RegisterUserForm()
    return render(request, 'registration.html', {'form': form})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы.')
            redirect_url = request.META.get('HTTP_REFERER')
        else:
            error_message = 'Некорректные введеные данные'
            params = {'error_message': 'Некорректные введеные данные', 'style': 'display :flex;'}
            redirect_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(f'{redirect_url}?error_message={error_message}&style=display:flex;')

        return HttpResponseRedirect(redirect_url)


@login_required
def logout_view(request):
    logout(request)
    redirect_url = 'index'  # request.GET.get('next', 'index') - возврат на страницу, с которой был выполнен логаут
    return redirect(redirect_url)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if user:
            login(request, user)
        response = super().post(request, *args, **kwargs)
        response.data['username'] = user.username
        return response


class CustomTokenRefreshView(TokenRefreshView):
    pass
