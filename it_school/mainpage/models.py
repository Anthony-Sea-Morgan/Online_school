from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    available_courses = models.TextField()
    wallet = 0
    is_student = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    courses = models.ManyToManyField('Course', blank=True)

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
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
