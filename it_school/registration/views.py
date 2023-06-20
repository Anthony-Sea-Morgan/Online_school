
from django.shortcuts import render, redirect
from .serializers import UserSerializer, LoginSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.views import View


@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            error_message = 'Invalid credentials'
            return render(request, 'loginn.html', {'error_message': error_message})
    else:
        return render(request, 'loginn.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('logged_out')
