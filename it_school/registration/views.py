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


@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('index')
        else:
            error_message = serializer.errors.get('password')[0] if serializer.errors.get('password') else 'Некорректные введенные данные'
            return render(request, 'registration.html', {'error_message': error_message})
    else:
        return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы.')
            return redirect('index')
        else:
            error_message = 'Некорректные введеные данные'
            return render(request, 'mainpage.html', {'error_message': error_message, 'style': 'display :flex;'})
    else:
        return render(request, 'mainpage.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
