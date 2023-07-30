from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from mainpage.models import Course, Lesson, CustomGroup
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import formset_factory
from mainpage.views import check_staff_permission, check_mentor_permission, add_users_in_group, remove_user_from_group
from django.urls import reverse_lazy, reverse
from mainpage.models import Course, Lesson, TECHNOLOGIES, CustomUser, TECHNOLOGY_CHOICES, DIFFICULTY_CHOICES, DAYS_OF_WEEK_CHOICES
from management.forms import CourseForm, LessonForm, CustomGroupForm, CustomUserListForm, LessonListForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from datetime import date

@method_decorator(check_staff_permission, name='dispatch')
class UserListView(View):
    template_name = 'user_list.html'
    formset_class = modelformset_factory(CustomUser, form=CustomUserListForm, extra=0)
    queryset = CustomUser.objects.all()
    def get(self, request):
        if request.user.is_superuser:
            self.queryset = CustomUser.objects.all()
        else:
            self.queryset = CustomUser.objects.exclude(is_staff=True).exclude(is_superuser=True)
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
                if not request.user.is_superuser:
                    instance.is_staff = False
                    instance.is_superuser = False
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

@method_decorator(check_mentor_permission, name='dispatch')
class LessonListView(View):

    template_name = 'lessons_list.html'
    formset_class = modelformset_factory(Lesson, form=LessonListForm, extra=0)
    queryset = Lesson.objects.all()
    def get(self, request, course_id):
        now = date.today()
        course = Course.objects.get(id=course_id)
        user = request.user
        if not user == course.mentor and not user.is_staff and not user.is_superuser:
            return render(request, 'access_deny.html')
        self.queryset = Lesson.objects.filter(course_owner=course)
        formset = self.formset_class(queryset=self.queryset)
        context = {
            'page_label': 'Список уроков курса',
            'formset': formset,
            'course': course,
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        now = date.today()
        course = Course.objects.get(id=course_id)
        formset = self.formset_class(request.POST, queryset=self.queryset)
        if formset.is_valid():
            instances = formset.save()
            for instance in instances:
                instance.save()
            return redirect(reverse('management:lessons_list', args=[course_id]))
        else:
            print(formset.errors)
        context = {
            'page_label': 'Список уроков курса',
            'formset': formset,
            'course': course,
        }
        return render(request, self.template_name, context)
@check_staff_permission
def CourseListView(request):
    user = request.user
    course_object = Course.objects.all()
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


@method_decorator(check_staff_permission, name='dispatch')
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

    def form_valid(self, form):
        self.object = form.save()
        user = self.object.mentor
        if add_users_in_group(user=user, course=self.object) == 0:
            user.save()
        return super().form_valid(form)


@method_decorator(check_staff_permission, name='dispatch')
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
        context['hide'] = 'hidden'
        self.prev_mentor = self.get_object().mentor
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('delete_course') == 'yes':
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                course = self.get_object()
                prev_mentor = course.mentor
                new_mentor = form.cleaned_data.get('mentor')
                if prev_mentor != new_mentor:
                    if remove_user_from_group(user=prev_mentor, course=course) == 0:
                        prev_mentor.save()
                    if add_users_in_group(user=new_mentor, course=course) == 0:
                        new_mentor.save()
                return super().post(request, *args, **kwargs)
            else:
                return self.form_invalid(form)

@check_mentor_permission
def remove_participant(request, pk):
    group = get_object_or_404(CustomGroup, course_owner_id=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        if not participant.is_staff or not participant.is_superuser:
            group.users.remove(participant)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('Invalid request method.')

@check_mentor_permission
def add_participant(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        participant_email = request.POST.get('participant_email')
        participant = get_object_or_404(CustomUser, email=participant_email)
        group.users.add(participant)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('Invalid request method.')

# def lesson_update(request, pk):
#     lesson = get_object_or_404(Lesson, pk=pk)
#     return HttpResponse("Lesson update view")
@method_decorator(check_staff_permission, name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('management:course_list')

@check_mentor_permission
def create_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    if not user == course.mentor and not user.is_staff and not user.is_superuser:
        return render(request, 'access_deny.html')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course_owner = course
            lesson.save()
            return redirect('management:lessons_list',course_id=course_id)  # Перенаправление на страницу деталей урока после успешного добавления
    else:
        form = LessonForm()

    context = {
        'form': form,
        'page_label': 'Добавить урок',
        'course_id': course.id,
    }
    return render(request, 'lesson_form.html', context)

@check_mentor_permission
def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course_owner_id
    user = request.user
    if not user == lesson.course_owner.mentor and not user.is_staff and not user.is_superuser:
        return render(request, 'access_deny.html')
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            return redirect('management:lessons_list', course_id=lesson.course_owner.id)
    else:
        form = LessonForm(instance=lesson)

    context = {
        'form': form,
        'page_label': 'Редактировать урок',
        'course_id': course_id,
    }
    return render(request, 'lesson_form.html', context)