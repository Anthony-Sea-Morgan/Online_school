from .models import Course, Lesson, TECHNOLOGIES
from registration.models import CustomUser
from django.forms import model_to_dict
from django.shortcuts import render, redirect
import os
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model

from django.shortcuts import render
from .models import Lesson
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@csrf_protect
def index(request):
    course_object = Course.objects.all()
    for i in course_object:
        i.img = str(i.img)[5:]
        i.imgTech = str(i.tech_img)[5:]
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    data = {
        'title': 'Online school',
        'page_label': 'Главная страница',
        'courses': course_object,
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
        'form': form,
    }
    template = 'mainpage.html'
    return render(request, template, data)


class CourseDetailView(DetailView):
    error = ''

    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'


def lesson_list(request):
    lessons = Lesson.objects.all()
    context = {'lessons': lessons}
    return render(request, 'lesson_list.html', context)


@login_required
def personal_cabinet(request):
    user = request.user
    courses = user.courses.all().order_by('start_date')  # Получаем список курсов пользователя, отсортированных по дате начала
    return render(request, 'personal_cabinet.html', {'user': user, 'courses': courses})
# @csrf_protect
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginUserForm(data=request.POST)
#         if form.is_valid():
#             user = form.cleaned_data.get('user')
#             login(request, user)
#             return redirect('index')
#     else:
#         form = LoginUserForm()
#     return render(request, 'index/login.html', {'form': form})
#
# @csrf_protect
# def logout_view(request):
#     logout(request)
#     return redirect('index')
#
# @csrf_protect
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'index/register.html', {'form': form})
