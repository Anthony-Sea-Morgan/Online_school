from django.shortcuts import render, redirect
from django.views import View
from mainpage.models import Course, Lesson, CustomGroup
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from mainpage.views import *
from django.urls import reverse_lazy, reverse
from mainpage.models import Course, Lesson, TECHNOLOGIES, CustomUser, TECHNOLOGY_CHOICES, DIFFICULTY_CHOICES, \
    DAYS_OF_WEEK_CHOICES
from management.forms import CourseForm, LessonForm, CustomGroupForm, CustomUserListForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class UserListView(View):
    template_name = 'user_list.html'
    form_class = CustomUserListForm
    queryset = CustomUser.objects.all()
    forms = []

    def get(self, request):
        forms = []
        for user in self.queryset:
            form = self.form_class(instance=user)
            forms.append((user, form))
        context = {
            'page_label': 'Список всех пользователей',
            'users_forms': forms,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        forms = []
        for user in self.queryset:
            form = self.form_class(request.POST, instance=user)
            if form.is_valid():
                if form.has_changed():
                    is_mentor = form.cleaned_data.get('is_mentor')
                    form.instance.is_student = not is_mentor
                    form.save()
            forms.append((user, form))
        context = {
            'page_label': 'Список всех пользователей',
            'users_forms': forms,
        }
        return redirect(reverse('management:user_list'))
@check_mentor_permission
def CourseListView(request):
    user = request.user
    course_object = Course.objects.filter(mentor=user)
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
    template = 'course_list.html'
    return render(request, template, data)


@method_decorator(check_mentor_permission, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('management:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentors'] = CustomUser.objects.all()
        context['technologies'] = TECHNOLOGY_CHOICES
        context['difficulty_choices'] = DIFFICULTY_CHOICES
        context['days_of_week_choices'] = DAYS_OF_WEEK_CHOICES
        context['lesson_form'] = LessonForm()
        context['group_form'] = CustomGroupForm()
        context['lessons'] = Lesson.objects.filter(course_owner=self.object)
        return context


@method_decorator(check_mentor_permission, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('management:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentors'] = CustomUser.objects.all()
        context['technologies'] = TECHNOLOGY_CHOICES
        context['difficulty_choices'] = DIFFICULTY_CHOICES
        context['days_of_week_choices'] = DAYS_OF_WEEK_CHOICES
        context['lesson_form'] = LessonForm()
        group = CustomGroup.objects.get(course_owner_id=self.kwargs['pk'])
        context['group'] = group
        context['lessons'] = Lesson.objects.filter(course_owner=self.object)
        return context

    def form_valid(self, form):
        if self.request.POST.get('delete_course') == 'yes':
            self.object = self.get_object()  # Получение текущего объекта
            self.object.delete()  # Удаление объекта
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.save(commit=False)
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())


def remove_participant(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        group.users.add(participant)
        return redirect('chat_room', room_name=pk)
    else:
        return redirect('chat_room', room_name=pk, error_message='пользователя с таким email адресом не существует', display = 'display:inherit')


def add_participant(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        group.users.remove(participant)
        return redirect('chat_room', room_name=pk)
    else:
        return redirect('chat_room', room_name=pk, error_message='пользователя с таким email адресом не существует', display = 'display:inherit')

# def lesson_update(request, pk):
#     lesson = get_object_or_404(Lesson, pk=pk)
#     return HttpResponse("Lesson update view")
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('management:course_list')


@method_decorator(check_mentor_permission, name='dispatch')
class LessonView(View):
    def get(self, request):
        lessons = Lesson.objects.all()
        return render(request, 'management/lesson.html', {'lessons': lessons})


@method_decorator(check_mentor_permission, name='dispatch')
def lesson_list(request):
    """
    Отображает список всех уроков.
    """
    now = date.today()
    lessons = Lesson.objects.all()
    context = {'lessons': lessons, 'now': now, 'page_label': 'Список всех занятий'}
    return render(request, 'lesson_list.html', context)
