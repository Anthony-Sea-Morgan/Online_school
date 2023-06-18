from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    wallet = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # кошелёк
    is_student = models.BooleanField(default=True)  # чекбокс является ли студентом
    is_mentor = models.BooleanField(default=not is_student)  # чекбокс является ли ментором
    courses = models.ManyToManyField('mainpage.Course', blank=True)  # список курсов к которому у порльзователя имеется доступ
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='customuser_set')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)  # телефонный номер с проверкой

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
