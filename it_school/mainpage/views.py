from tabulate import tabulate
from datetime import date

from .models import Course, Lesson, CustomGroup, CustomUser, Review, Attendance, ChatMessage, TECHNOLOGIES
from .forms import ProfileForm, WalletForm, CourseReviewForm
from django.utils.decorators import method_decorator
from django.utils import timezone
import calendar
from django.db.models import Q
from itertools import groupby, islice
from operator import attrgetter
from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import user_passes_test


def check_mentor_permission(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_mentor:
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return wrapped_view
def check_staff_permission(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')  # Перенаправление на главную страницу
        return view_func(request, *args, **kwargs)

    return wrapped_view
def check_superuser_permission(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')  # Перенаправление на главную страницу
        return view_func(request, *args, **kwargs)

    return wrapped_view


@csrf_protect
def index(request):
    """
    Отображает главную страницу и список курсов.
    """
    current_date = date.today()
    closest_courses = Course.objects.filter(start_date__gte=current_date)
    closest_courses = closest_courses.order_by('start_date').order_by('-rating')[:5]
    for i in closest_courses:
        i.img = str(i.img)
    data = {
        'title': 'Online school',
        'page_label': 'Главная страница',
        'courses': closest_courses,
    }
    template = 'mainpage.html'
    return render(request, template, data)

@csrf_protect
def courses_list(request):
    """
    Отображает главную страницу и список курсов.
    """
    course_object = Course.objects.all()
    for i in course_object:
        i.img = str(i.img)
    data = {
        'title': 'Online school',
        'page_label': 'Доступные курсы',
        'courses': course_object,
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
    }
    template = 'courses_list.html'
    return render(request, template, data)


@login_required
def course_lessons(request, course_id):
    """
    Отображает список уроков для определенного курса.
    """
    user = request.user
    now = date.today()

    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course_owner=course)
    reviews = Review.objects.filter(course=course).order_by('-rating')[:5]

    is_course_owner = course.mentor == user
    is_course_added = user.courses.filter(id=course_id).exists()


    if is_course_owner is False and is_course_added is False and not user.is_staff and not user.is_superuser:
        return render(request, 'access_deny.html')
    review = None
    form_save_btn = "Оставить отзыв"
    try:
        review = Review.objects.get(course=course, user=user)
        form = CourseReviewForm(instance=review)
        form_save_btn = "Изменить отзыв"
    except Review.DoesNotExist:
        form = CourseReviewForm()

    if request.method == 'POST':
        # Если форма отправлена
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            if review:
                review.text = form.cleaned_data['text']
                review.rating = form.cleaned_data['rating']
                review.save()
            else:
                # Если отзыва нет, создаем новый
                review = form.save(commit=False)
                review.user = user
                review.course = course
                review.save()

            form = CourseReviewForm()
        return redirect('course_lessons', course_id=course_id)

    return render(request, 'course_lessons.html', {
                    'course': course,
                    'page_label': 'Список уроков курса',
                    'lessons': lessons,
                    'now': now,
                    'form': form,
                    'reviews': reviews,
                    'review': review,
                    'form_save_btn': form_save_btn,
                   })


@login_required
def personal_cabinet(request):
    """
     Отображает личный кабинет пользователя.
    """
    user = request.user
    courses = user.courses.all().order_by(
        'start_date')
    lessons_by_course = {}
    all_lessons = Lesson.objects.all()
    for course in courses:
        lessons = all_lessons.filter(course_owner=course)
        lessons_by_course[course] = lessons

    now = timezone.now()
    user_courses = user.courses.all()
    user_lessons = all_lessons.filter(course_owner__in=user_courses)
    sorted_lessons = sorted(user_lessons.filter(Q(start_date__gte=now.date()) | Q(start_date=now.date(), start_time__gte=now.time())), key=attrgetter('start_date'))
    grouped_lessons = {date: list(lessons) for date, lessons in islice(groupby(sorted_lessons, key=attrgetter('start_date')), 4)}

    wallet_form = WalletForm()
    edit_form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        wallet_form = WalletForm(request.POST, instance=request.user)
        edit_form = ProfileForm(request.POST, instance=request.user)
        if wallet_form.is_valid():
            wallet_form.save()
            return redirect('personal_cabinet')
        if edit_form.is_valid():
            edit_form.save()
            return redirect('personal_cabinet')
    else:
        edit_form = ProfileForm(instance=request.user)
    context = {
        'user': user,
        'courses': courses,
        'lessons_by_course': lessons_by_course,
        'wallet_form': wallet_form,
        'edit_form': edit_form,
        'page_label': 'Личный кабинет',
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
        'grouped_lessons': grouped_lessons,
    }
    return render(request, 'personal_cabinet.html',context)



@csrf_protect
def about_us_view(request):
    """
    Отображает страницу "О нас".
    """
    return render(request, 'about.html', {'page_label': 'Информация о нас'})

@method_decorator(csrf_protect, name='dispatch')
class CourseDetailView(DetailView):
    """
    Класс-представление для отображения детальной информации о курсе.
    """
    error = ''
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.courses.filter(pk=self.get_object().pk).exists():
                return redirect('index')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'confirm_payment' in request.POST:
            course = self.get_object()
            user = request.user
            course_price = course.price

            if user.wallet >= course_price:
                if add_users_in_group(user=user, course=course) == 0:
                    user.wallet -= course_price
                    user.save()
                    subject = 'Запись на курс успешна'
                    html_message = render_to_string('email_templates/purchase_confirmation_email.html')
                    plain_message = strip_tags(html_message)
                    from_email = 'norepy.onlinecourses@gmail.com'
                    to_email = user.email
                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                    messages.success(request, 'Оплата прошла успешно.')
                    return redirect('purchase_confirmation', pk=course.pk)
                else:
                    messages.success(request, 'Вы разве не купили уже этот курс?')
                    return redirect('purchase_confirmation', pk=course.pk)
            else:
                self.error = 'Недостаточно средств на счете.'

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.error
        context['page_label'] = 'Информация о курсе'
        course = self.get_object()
        context['reviews'] = Review.objects.filter(course=course).order_by('-rating')[:5]
        if self.error:
            context['styleconfp'] = 'display: flex;'
        return context


def add_users_in_group(user, course):
    try:
        group = CustomGroup.objects.filter(course_owner=course.pk).first()
        if group is not None:
            if user.courses.filter(pk=course.pk).exists():
                # Пользователь уже добавлен в курс
                if user in group.users.all():
                    return 1
                else:
                    group.users.add(user)
                    return 1
            else:
                user.courses.add(course)
                group.users.add(user)
                print(f'{user} добавлен {course} с группой {group}')
                return 0
        else:
            # Группа не найдена
            return 1
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1


def remove_user_from_group(user, course):
    try:
        group = CustomGroup.objects.filter(course_owner=course.pk).first()
        if group is not None:
            if user.courses.filter(pk=course.pk).exists():
                # Удаляем пользователя из курса
                user.courses.remove(course)
                # Удаляем пользователя из группы
                group.users.remove(user)
                print(f'{user} удален из {course} и группы {group}')
                return 0
            else:
                # Пользователь не найден в курсе
                return 1
        else:
            # Группа не найдена
            return 1
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
@login_required
def purchase_confirmation(request, pk):
    """
    Отображает страницу подтверждения покупки курса.
    """
    course = Course.objects.get(id=pk)
    return render(request, 'purchase_confirmation.html', {'course': course})


@login_required
def attendance_table(request):
    """
    Отображает таблицу посещаемости для всех групп.
    """
    user = request.user
    if not user.is_mentor:
        return render(request, 'access_deny.html')
    groups = CustomGroup.objects.all()
    attendance_tables = []

    for group in groups:
        lessons = Lesson.objects.filter(course_owner=group.course_owner)
        students = CustomUser.objects.filter(groups=group)
        attendance = Attendance.objects.filter(group=group)

        print(f'{students}')

        table = []
        table_headers = ['Слушатель'] + [str(lesson.start_date) for lesson in lessons]

        for student in students:
            row = [student.get_full_name()]
            for lesson in lessons:
                attendance_entry = attendance.get(lesson=lesson, student=student)
                row.append(attendance_entry.attended)
            table.append(row)

        attendance_tables.append({
            'group': group,
            'table': tabulate(table, headers=table_headers, tablefmt='grid')
        })

    return render(request, 'attendance.html',
                  {'attendance_tables': attendance_tables, 'page_label': 'Журнал посещения'})




