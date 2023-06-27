from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model


class ChatMessage(models.Model):
    text = models.TextField()
    author = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE)
    #group = models.ForeignKey('mainpage.CustomGroup', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
