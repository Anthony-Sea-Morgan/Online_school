from .models import Course, Lesson, TECHNOLOGIES
from registration.models import CustomUser
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib import messages
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

    def post(self, request, *args, **kwargs):
        if 'confirm_payment' in request.POST:
            course = self.get_object()
            user = request.user
            course_price = course.price

            if user.wallet >= course_price:
                user.wallet -= course_price
                user.save()
                messages.success(request, 'Оплата прошла успешно.')
                return redirect('purchase_confirmation', pk=course.pk)
            else:
                self.error = 'Недостаточно средств на счете.'

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.error
        if self.error:
            context['styleconfp'] = 'display: flex;'
        return context

def purchase_confirmation(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'purchase_confirmation.html', {'course': course})