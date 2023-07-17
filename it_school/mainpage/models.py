from uuid import uuid4
from logging import getLogger
from datetime import datetime, time, timedelta

from django.contrib.auth.models import Group
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from .fields import WEBPField
from django.contrib import admin
from registration.models import CustomUser
from django.db import models
from django.utils import timezone

DAYS_OF_WEEK_CHOICES = [
    ('monday', 'понедельник'),
    ('tuesday', 'вторник'),
    ('wednesday', 'среда'),
    ('thursday', 'четверг'),
    ('friday', 'пятница'),
    ('saturday', 'суббота'),
    ('sunday', 'воскресенье'),
]
TECHNOLOGIES = ['Python', 'C++', 'Java', 'C#', 'Pascal', 'Frontend']
TECHNOLOGY_CHOICES = [(tech, tech) for tech in TECHNOLOGIES]
DIFFICULTY_CHOICES = [
    ('Начинающий', 'Beginner'),
    ('Продвинутый', 'Advanced'),
]
logger = getLogger(__name__)


# Функция для определения пути сохранения изображения курса
def image_folder_Course(instance, filename):
    return 'Models/Course/CourseIcons/{}.webp'.format(uuid4().hex)


# Функция для определения пути сохранения изображения языка
def image_folder_Technology(instance, filename):
    return 'Models/Course/TechIcons/{}.webp'.format(uuid4().hex)


class Course(models.Model):
    title = models.CharField(max_length=50)  # Тема курса
    description = models.TextField('Полное описание', blank=True)  # Описание
    short_des = models.TextField('Краткое описание', default='', max_length=100)
    difficulty = models.CharField('Сложность курса', max_length=15, choices=DIFFICULTY_CHOICES)  # Сложность
    rating = models.DecimalField('Рейтинг курса', max_digits=3, decimal_places=1)  # Рейтинг(оценка) курса
    price = models.DecimalField('Стоимость курса', max_digits=6, decimal_places=2)  # Стоимость курса
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField('Дата начала курса', default=timezone.now)  # Поле даты начала курса
    start_time = models.TimeField('Время начала курса', default=time(19, 0))  # Поле времени начала курса
    days_of_week = MultiSelectField('Дни недели занятий', choices=DAYS_OF_WEEK_CHOICES,
                                    validators=[MaxValueValidator(7)],
                                    default='monday')  # Чекбоксы для выбора дней недели
    technologies = MultiSelectField('Применяемы языки', choices=TECHNOLOGY_CHOICES,
                                    validators=[MaxValueValidator(5)],
                                    default='Python')  # Чекбоксы для выбора дней недели
    lessons_count = models.IntegerField(default=1)  # Кол-во уроков в курсе
    img = WEBPField(  # изображение курса
        verbose_name=('Изображение курса'),
        upload_to=image_folder_Course,
        default='media/Models/no_image_big.png',
    )
    tech_img = WEBPField(  # изображение языка
        verbose_name=('Изображение языка'),
        upload_to=image_folder_Technology,
        default='media/Models/no_image_big.png',
    )

    def save(self, *args, **kwargs):
        """Функция срабатывает при сохранении курса
        В функции происходит создание Занятий, согласно их количеству.
        При редактировании количества занятий, либо добавляются новые, либо удаляются последние.
        """
        if not self.mentor.is_mentor:
            logger.warning("Пользователь не является ментором")
            return 1
        if not self.days_of_week:
            self.days_of_week = ['wednesday', 'saturday']

        is_created = not bool(self.pk)

        super().save(*args, **kwargs)

        lesson_count = Lesson.objects.filter(course_owner_id=self.pk).count()

        if is_created:
            group = CustomGroup.objects.create(course_owner=self, name=f'{self.title}.{self.difficulty}.Группа.')
            logger.info(f'Создана группа: {group.pk}')
            next_date = self.start_date
            for i in range(self.lessons_count):
                count = len(self.days_of_week)
                day = i % count

                if isinstance(self.days_of_week, set):
                    self.days_of_week = list(self.days_of_week)

                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += timedelta(days=1)

                Lesson.objects.create(course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day], start_date=next_date.isoformat(),
                                      start_time=self.start_time)
        elif lesson_count < self.lessons_count:

            last_lesson = Lesson.objects.filter(course_owner=self).order_by('-pk').first()
            next_date = last_lesson.start_date

            for i in range(lesson_count, self.lessons_count):
                count = len(self.days_of_week)
                day = i % count

                if isinstance(self.days_of_week, set):
                    self.days_of_week = list(self.days_of_week)
                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += timedelta(days=1)

                Lesson.objects.create(course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day], start_date=next_date,
                                      start_time=self.start_time)

        elif lesson_count > self.lessons_count:
            for i in range(self.lessons_count, lesson_count):
                last_lesson = Lesson.objects.filter(course_owner=self).order_by('-pk').first()
                if last_lesson:
                    last_lesson.delete()

    @staticmethod
    def get_weekday_index(weekday):
        return {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}[
            weekday]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course_owner = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_course',
                                     null=False, editable=False)  # Курс, к которому принадлежит занятие
    mentor_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_mentor',
                                     null=False,
                                     default=1)  # Ментор, который проводит занятие
    title = models.CharField(max_length=255, default='Lesson 1', blank=True)
    material = models.TextField('Полное описание', default='Полное описание')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES, default='monday')
    start_date = models.DateField(default=timezone.now)
    start_time = models.TimeField('Время начала курса', default=time(19, 0))
    is_past = models.BooleanField(default=False, editable=False)

    def is_past_lesson(self):
        return self.start_date < timezone.now().date()

    def __str__(self):
        return str(f'{self.title}')

    def save(self, *args, **kwargs):
        if self.mentor_owner.is_mentor:
            super().save(*args, **kwargs)
        else:
            logger.warning("Пользователь не является ментором")

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class CustomGroup(Group):
    course_owner = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='group_course',
                                     default=1)  # Курс, к которому принадлежит группа
    description = models.TextField(blank=True)
    users = models.ManyToManyField(CustomUser, related_name='custom_groups')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return str(f'{self.name}')


class CustomGroupAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('users')  # Включаем связанных пользователей (это оптимизация запроса)
        return queryset

    def get_users_list(self, obj):
        return ", ".join(user.username for user in obj.users.all())

    get_users_list.short_description = 'Пользователи'

    def users_list(self, obj):
        return self.get_users_list(obj)

    list_display = ['name', 'users_list']


class Review(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews', null=False)
    title = models.CharField(max_length=1000, blank=False)
    objective = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objective', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('lesson', 'group', 'student')


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='sent_messages')  # Отправитель сообщения
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)  # Группа, к которой относится сообщение
    text = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Дата и время отправки сообщения
    is_mentor = models.BooleanField(default=False)
