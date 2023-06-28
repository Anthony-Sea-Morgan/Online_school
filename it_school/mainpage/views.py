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


@csrf_protect
def index(request):
    course_object = Course.objects.all()
    for i in course_object:
        i.img = str(i.img)[5:]
        i.imgTech = str(i.tech_img)[5:]
    data = {
        'title': 'Online school',
        'page_label': 'Главная страница',
        'courses': course_object,
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
    }
    template = 'mainpage.html'
    return render(request, template, data)


class CourseDetailView(DetailView):
    error = ''

    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

