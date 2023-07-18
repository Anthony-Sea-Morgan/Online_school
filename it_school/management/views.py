from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from mainpage.models import Course, Lesson, CustomGroup
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import formset_factory
from mainpage.views import *
from django.urls import reverse_lazy, reverse
from mainpage.models import Course, Lesson, TECHNOLOGIES, CustomUser, TECHNOLOGY_CHOICES, DIFFICULTY_CHOICES, DAYS_OF_WEEK_CHOICES
from management.forms import CourseForm, LessonForm, CustomGroupForm, CustomUserListForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class UserListView(View):
    template_name = 'user_list.html'
    formset_class = modelformset_factory(CustomUser, form=CustomUserListForm, extra=0)
    queryset = CustomUser.objects.all()

    def get(self, request):
        formset = self.formset_class(queryset=self.queryset)
        context = {
            'page_label': 'Список всех пользователей',
            'formset': formset,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        formset = self.formset_class(request.POST, queryset=self.queryset)
        if formset.is_valid():
            instances = formset.save()
            for instance in instances:
                is_mentor = instance.is_mentor
                instance.is_student = not is_mentor
                print("Username:", instance.username)
                print("Email:", instance.email)
                print("First Name:", instance.first_name)
                print("Last Name:", instance.last_name)
                instance.save()
            return redirect(reverse('management:user_list'))
        else:
            print(formset.errors)
        context = {
            'page_label': 'Список всех пользователей',
            'formset': formset,
        }
        return render(request, self.template_name, context)
@check_mentor_permission
def CourseListView(request):
    user = request.user
    course_object = Course.objects.filter(mentor=user)
    for i in course_object:
        i.img = str(i.img)[5:]
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
        context['view_name'] = self.request.resolver_match.view_name
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
        context['view_name'] = self.request.resolver_match.view_name
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('delete_course') == 'yes':
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


def remove_participant(request, pk):
    group = get_object_or_404(CustomGroup, course_owner_id=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        group.users.remove(participant)
        return redirect('chat_room', room_name=pk)
    else:
        raise Http404('Invalid request method.')


def add_participant(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        group.users.add(participant)
        return redirect('chat_room', room_name=pk)
    else:
        raise Http404('Invalid request method.')

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
