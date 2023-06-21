from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

from registration.models import *
from mainpage.models import *
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'material')


# Register your models here.
admin.site.register(Course, PostAdmin)
admin.site.register(Lesson)
admin.site.register(CustomUser)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.unregister(Group)
admin.site.register(Review)
