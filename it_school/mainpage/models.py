import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator


class CustomUser(AbstractUser):
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # кошелёк
    is_student = models.BooleanField(default=True)  # является студентом
    is_mentor = models.BooleanField(default=not is_student)  # является ментором
    courses = models.ManyToManyField('Course', blank=True)  # список курсов к которому у порльзователя имеется доступ
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='customuser_set')  #
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='customuser_set')

    def __str__(self):
        return self.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    DIFFICULTY_CHOICES = [
        ('beginner', 'Начинающий'),
        ('advanced', 'Продвинутый'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    mentor = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today())  # Поле даты начала курса
    start_time = models.TimeField(default=datetime.time(19, 0))  # Поле времени начала курса
    DAYS_OF_WEEK_CHOICES = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK_CHOICES,
                                    validators=[MaxValueValidator(7)], default='monday')  # Поле для выбора дней недели
    lessons_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.days_of_week:
            self.days_of_week = ['wednesday', 'saturday' ]
        tmp_pk = self.pk
        is_created = not self.pk
        super().save(*args, **kwargs)
        if is_created:
            for i in range(self.lessons_count):
                Lesson.objects.create(course_owner=self, title=f'{self.title}. Lesson {i + 1}')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course_owner = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons', null=False)
    title = models.CharField(max_length=255, default='Lesson 1', blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.title)
