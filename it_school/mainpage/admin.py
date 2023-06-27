from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from registration.models import *
from mainpage.models import *
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'material')

# Register your models here.
admin.site.register(Course, PostAdmin)
admin.site.register(Lesson, PostAdmin)
admin.site.register(CustomUser)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.unregister(Group)
admin.site.register(Review)
