from mainpage.models import *
from django_summernote.admin import SummernoteModelAdmin
from django import forms
from django.contrib import admin
from .models import Course, CustomUser

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentor'].queryset = CustomUser.objects.filter(is_mentor=True)

class CourseAdmin(SummernoteModelAdmin):
    form = CourseAdminForm
    summernote_fields = ('description', 'material')


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'material')


# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, PostAdmin)
admin.site.register(CustomUser)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.unregister(Group)
admin.site.register(Review)
admin.site.register(Attendance)
admin.site.register(ChatMessage)
