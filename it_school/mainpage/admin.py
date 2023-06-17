from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from .models import Course


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)


# Register your models here.
admin.site.register(Course, PostAdmin)
admin.site.register(Lesson)
admin.site.register(CustomUser)
