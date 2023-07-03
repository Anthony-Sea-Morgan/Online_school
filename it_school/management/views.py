from django.shortcuts import render
from django.views import View
from mainpage.models import Course, Lesson, CustomGroup
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
class CourseListView(ListView):
    model = Course
    template_name = 'manage_page.html'
    context_object_name = 'courses'

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
    template_name = 'management/course_form.html'
    fields = '__all__'

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