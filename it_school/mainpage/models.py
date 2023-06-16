import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

DAYS_OF_WEEK_CHOICES = [
    ('monday', 'понедельник'),
    ('tuesday', 'вторник'),
    ('wednesday', 'среда'),
    ('thursday', 'четверг'),
    ('friday', 'пятница'),
    ('saturday', 'суббота'),
    ('sunday', 'воскресенье'),
]


class CustomUser(AbstractUser):
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # кошелёк
    is_student = models.BooleanField(default=True)  # является студентом
    is_mentor = models.BooleanField(default=not is_student)  # является ментором
    courses = models.ManyToManyField('Course', blank=True)  # список курсов к которому у порльзователя имеется доступ
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='customuser_set')  #
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='customuser_set')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Начинающий'),
        ('Advanced', 'Продвинутый'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    mentor = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)  # Поле даты начала курса
    start_time = models.TimeField(default=datetime.time(19, 0))  # Поле времени начала курса

    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK_CHOICES,
                                    validators=[MaxValueValidator(7)], default='monday')  # Поле для выбора дней недели
    lessons_count = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.days_of_week:
            self.days_of_week = ['wednesday', 'saturday']
        is_created = not bool(self.pk)
        super().save(*args, **kwargs)
        lesson_count = Lesson.objects.filter(course_owner_id=self.pk).count()
        max_pk = Lesson.objects.filter(course_owner=self).aggregate(max_pk=models.Max('pk'))['max_pk']
        initial_i = max_pk + 1 if max_pk is not None else 0
        if is_created:
            for i in range(self.lessons_count):
                count = len(self.days_of_week)
                day = i % count
                Lesson.objects.create(pk=initial_i, course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day])
                initial_i += 1
        elif lesson_count < self.lessons_count:
            for i in range(lesson_count, self.lessons_count):
                count = len(self.days_of_week)
                day = i % count
                Lesson.objects.create(pk=initial_i, course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day])
                initial_i += 1
        elif lesson_count > self.lessons_count:
            for i in range(self.lessons_count, lesson_count):
                Lesson.objects.filter(pk=initial_i - 1).delete()
                initial_i -= 1

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course_owner = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lesson_course', null=False)
    mentor_owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='lesson_mentor', null=False,
                                     default=1)

    title = models.CharField(max_length=255, default='Lesson 1', blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES, default='monday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class Review(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='reviews', null=False)
    title = models.CharField(max_length=1000, blank=False)
    objective = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='objective', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
