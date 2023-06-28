import datetime
import uuid
import logging
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.utils import timezone
from .fields import WEBPField
from django.db import models
from registration.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib import admin

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
logger = logging.getLogger(__name__)


def image_folder_Course(instance, filename):
    return 'mainpage/static/dist/img/Models/Course/CourseIcons/{}.webp'.format(uuid.uuid4().hex)


def image_folder_Technology(instance, filename):
    return 'mainpage/static/dist/img/Models/Course/TechIcons/{}.webp'.format(uuid.uuid4().hex)


class Course(models.Model):
    title = models.CharField(max_length=100)  # Тема курса
    description = models.TextField('Полное описание')  # Описание
    short_des = models.TextField('Краткое описание', default='')

    difficulty = models.CharField('Сложность курса', max_length=15, choices=DIFFICULTY_CHOICES)  # Сложность
    rating = models.DecimalField('Рейтинг курса', max_digits=3, decimal_places=1)  # Рейтинг(оценка) курса
    price = models.DecimalField('Стоимость курса', max_digits=6, decimal_places=2)  # Стоимость курса
    mentor = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE)

    start_date = models.DateField('Дата начала курса', default=timezone.now)  # Поле даты начала курса
    start_time = models.TimeField('Время начала курса', default=datetime.time(19, 0))  # Поле времени начала курса

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
        default='mainpage/static/dist/img/Models/no_image_big.png',
    )
    tech_img = WEBPField(  # изображение языка
        verbose_name=('Изображение языка'),
        upload_to=image_folder_Technology,
        default='mainpage/static/dist/img/Models/no_image_big.png',
    )

    def save(self, *args, **kwargs):
        """Функция срабатывает при сохранении курса
        В функции происходит создание Занятий, согласно их количеству.
        При редактировании количества занятий, либо добавляются новые, либо удаляются последние.
        """
        if self.mentor.is_mentor != True:
            print("Пользователь не является ментором")
            return 1
        if not self.days_of_week:
            self.days_of_week = ['wednesday', 'saturday']

        is_created = not bool(self.pk)

        try:
            super().save(*args, **kwargs)
        except Exception as e:
            pass
        lesson_count = Lesson.objects.filter(course_owner_id=self.pk).count()

        if is_created:
            CustomGroup.objects.create(course_owner=self, name=f'{self.title}.{self.difficulty}.Группа.')
            next_date = self.start_date
            for i in range(self.lessons_count):
                count = len(self.days_of_week)
                day = i % count

                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += datetime.timedelta(days=1)

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
                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += datetime.timedelta(days=1)
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
    course_owner = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lesson_course',
                                     null=False, editable=False)  # Курс, к которому принадлежит занятие
    mentor_owner = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='lesson_mentor',
                                     null=False,
                                     default=1)  # Ментор, который проводит занятие

    title = models.CharField(max_length=255, default='Lesson 1', blank=True)  # Название занятия
    material = models.TextField('Полное описание', default='Полное описание')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES, default='monday')  # день недели
    start_date = models.DateField(default=timezone.now)  # Поле даты начала занятия
    start_time = models.TimeField(default=datetime.time(19, 0))  # Поле времени начала занятия

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(f'{self.title}')

    def save(self, *args, **kwargs):
        if self.mentor_owner.is_mentor:
            super().save(*args, **kwargs)
        else:
            print("Пользователь не является ментором!")

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class CustomGroup(Group):
    course_owner = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='group_course',
                                     null=True)  # Курс, к которому принадлежит группа
    description = models.TextField(blank=True)
    users = models.ManyToManyField('registration.CustomUser', related_name='custom_groups')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


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
    owner = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='reviews', null=False)
    title = models.CharField(max_length=1000, blank=False)
    objective = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='objective', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


# Сигналы Django
@receiver(m2m_changed, sender=CustomUser.courses.through)
def handle_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Функция выполняется когда пользователю добавляется курс
    :param sender: источник сигнала
    :param instance: конкретный пользователь
    :param action: действие  - добавление связей
    :param reverse: обратная связь
    :param model: модель с которой связывают
    :param pk_set: множество ключей с колторыми связывают
    :param kwargs: прочие параметры
    :return: нет
    """
    if action == 'post_add':
        # Обработка добавления курса
        for pk in pk_set:
            course = model.objects.get(pk=pk)
            try:
                group = CustomGroup.objects.get(course_owner=pk)
                # Добавить в группу пользователя
                group.users.add(instance)
                print(f'Пользователь {instance.username} записался на курс {course.title} в группу {group.name}')
            except Exception as e:
                print(f'Не найдена группа для курса {str(e)}')
    elif action == 'post_remove':
        # Обработка удаления курса
        for pk in pk_set:
            course = model.objects.get(pk=pk)
            # Выполнить нужные действия после удаления курса
            if course is not None:
                print(f'Пользователь {instance.username} отписался с курса {course.title}')


@receiver(pre_save, sender=Course)
def update_lessons_mentor(sender, instance, **kwargs):
    if instance.pk:  # Проверяем, что модель уже существует (не новая)
        previous_mentor = Course.objects.get(pk=instance.pk).mentor  # Получаем предыдущего ментора
        if previous_mentor != instance.mentor:  # Если ментор изменился
            Lesson.objects.filter(course_owner=instance).update(
                mentor_owner=instance.mentor)  # Обновляем ментора у всех занятий данного курса
