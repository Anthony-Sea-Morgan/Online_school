from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    available_courses = models.TextField()
    wallet = models.IntegerField(default=0)
    is_student = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    courses = models.ManyToManyField('Course', blank=True)
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='customuser_set')
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

    def __str__(self):
        return self.title
