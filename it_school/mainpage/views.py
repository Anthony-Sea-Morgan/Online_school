from tabulate import tabulate
from datetime import date

from .models import Course, Lesson, CustomGroup, CustomUser, Attendance, ChatMessage, TECHNOLOGIES
from .forms import ProfileForm

from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@csrf_protect
def index(request):
    """
    Отображает главную страницу и список курсов.
    """
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


@login_required
def lesson_list(request):
    """
    Отображает список всех уроков.
    """
    now = date.today()
    lessons = Lesson.objects.all()
    context = {'lessons': lessons, 'now': now}
    return render(request, 'lesson_list.html', context)


@login_required
def course_lessons(request, course_id):
    """
    Отображает список уроков для определенного курса.
    """
    now = date.today()
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course_owner=course)
    return render(request, 'course_lissons.html', {'course': course, 'lessons': lessons, 'now': now})


@login_required
def personal_cabinet(request):
    """
     Отображает личный кабинет пользователя.
     """
    user = request.user
    courses = user.courses.all().order_by(
        'start_date')  # Получаем список курсов пользователя, отсортированных по дате начала

    # Создаем пустой словарь для хранения уроков по курсам
    lessons_by_course = {}

    # Получаем список уроков для каждого курса
    for course in courses:
        lessons = Lesson.objects.filter(course_owner=course)
        lessons_by_course[course] = lessons

    return render(request, 'personal_cabinet.html',
                  {'user': user, 'courses': courses, 'lessons_by_course': lessons_by_course})


@login_required
def edit_profile(request):
    """
    Отображает форму редактирования профиля пользователя и обрабатывает ее сохранение.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('personal_cabinet')  # Перенаправление на личный кабинет после сохранения
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


def about_us_view(request):
    """
    Отображает страницу "О нас".
    """
    return render(request, 'about.html')


class CourseDetailView(DetailView):
    """
    Класс-представление для отображения детальной информации о курсе.
    """
    error = ''
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get(self, request, *args, **kwargs):
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

    return render(request, 'attendance.html', {'attendance_tables': attendance_tables})


def check_mentor_permission(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_mentor:
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return wrapped_view


@login_required
def chat_room(request, group_id):
    """
    Отображает комнату чата для определенной группы.
    """
    group = get_object_or_404(CustomGroup, id=group_id)
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'room.html', {'group': group, 'messages': messages})


@login_required
def send_message(request, group_id):
    """
    Отправляет сообщение в чат для определенной группы.
    """
    if request.method == 'POST':
        group = get_object_or_404(CustomGroup, id=group_id)
        sender = request.user
        message_text = request.POST.get('message_text')
        if message_text:
            ChatMessage.objects.create(sender=sender, group=group, text=message_text)
    return redirect('chat_room', group_id=group_id)
