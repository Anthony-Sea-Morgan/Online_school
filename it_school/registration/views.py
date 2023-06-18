from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import CustomUser
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешной авторизации
        return render(request, 'registration.html', {'form': form})
