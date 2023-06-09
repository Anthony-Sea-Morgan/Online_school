from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    available_courses = models.TextField()
    wallet = 0
    is_student = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
