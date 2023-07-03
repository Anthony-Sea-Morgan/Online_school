from django.shortcuts import render
from django.views import View
from mainpage.models import Course, Lesson, CustomGroup
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mainpage.models import Course, Lesson, TECHNOLOGIES, CustomUser, TECHNOLOGY_CHOICES,DIFFICULTY_CHOICES, DAYS_OF_WEEK_CHOICES
from .forms import CourseForm
from django.http import HttpResponseRedirect
def CourseListView(request):
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
    template = 'manage_page.html'
    return render(request, template, data)

class CourseCreateView(CreateView):
    model = Course
    template_name = 'management/course_form.html'
    fields = '__all__'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'management/course_detail.html'
    context_object_name = 'course'

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('management:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentors'] = CustomUser.objects.all()
        context['technology_choices'] = TECHNOLOGY_CHOICES
        context['difficulty_choices'] = DIFFICULTY_CHOICES
        context['days_of_week_choices'] = DAYS_OF_WEEK_CHOICES
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Сохранение формы без коммита
        self.object.save()  # Сохранение изменений в модели
        return HttpResponseRedirect(self.get_success_url())

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('management:course_list')

class LessonView(View):
    def get(self, request):
        lessons = Lesson.objects.all()
        return render(request, 'management/lesson.html', {'lessons': lessons})

class CustomGroupView(View):
    def get(self, request):
        custom_groups = CustomGroup.objects.all()
        return render(request, 'management/custom_group.html', {'custom_groups': custom_groups})