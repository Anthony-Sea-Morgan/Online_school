from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from mainpage.models import Course, Lesson, CustomGroup
from registration.models import CustomUser
from django.forms import ModelForm, TextInput, Textarea,  ClearableFileInput, formset_factory
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _("")
    initial_text = _("")
    input_text = _("Изображение курса")
    template_name = "custom_clearable_file_input.html"

class CourseForm(forms.ModelForm):
    mentor = forms.ModelChoiceField(queryset=get_user_model().objects.filter(is_mentor=True),
                                    widget=forms.Select(attrs={'class': 'form-group'}))
    class Meta:
        model = Course
        fields = ['title', 'description', 'short_des', 'lessons_count', 'difficulty', 'technologies', 'price', 'mentor', 'start_date','start_time', 'days_of_week', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'description': SummernoteWidget(attrs={'class': 'form-group'}),
            'short_des': forms.Textarea(attrs={'class': 'form-group'}),
            'difficulty': forms.Select(attrs={'class': 'form-group'}),
            'lessons_count': forms.NumberInput(attrs={'class': 'form-group', 'type':'number'}),
            'price': forms.NumberInput(attrs={'class': 'form-group', 'type':'number'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group','id': 'id_start_date', 'name': 'start_date', 'type':'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group','id': 'id_start_time', 'name': 'start_time', 'type':'time'}),
            'days_of_week': forms.CheckboxSelectMultiple(attrs={'class': 'form-group', 'style':'width: 5%;height: 100%;'}),
            'technologies': forms.CheckboxSelectMultiple(attrs={'class': 'form-group', 'style':'width: 5%;height: 100%;'}),
            'img': CustomClearableFileInput(attrs={'class': "file-input", 'id': "img", 'value': ""}),
        }

class LessonListForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['id', 'mentor_owner', 'title', 'start_date', 'start_time']
        widgets = {
            'id': forms.NumberInput(attrs={'class': 'form-group', 'type': 'number'}),
            'mentor_owner': forms.Select(attrs={'class': 'form-group'}),
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group','id': 'id_start_date', 'name': 'start_date', 'type':'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group','id': 'id_start_time', 'name': 'start_time', 'type':'time'}),
        }
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'material', 'start_date', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'material': SummernoteWidget(attrs={'class': 'form-group'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group', 'id': 'id_start_date', 'name': 'start_date', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group', 'id': 'id_start_time', 'name': 'start_time', 'type': 'time'}),
        }

class CustomGroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['course_owner', 'name', 'description', 'users']
        widgets = {
            'course_owner': forms.Select(attrs={'class': 'form-group'}),
            'name': forms.TextInput(attrs={'class': 'form-group'}),
            'description': forms.Textarea(attrs={'class': 'form-group'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-group'}),
        }
class CustomUserListForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('is_superuser', 'is_mentor', 'is_staff', 'wallet', 'is_student', 'username', 'email', 'first_name', 'last_name')
        widgets ={
            'is_superuser': forms.CheckboxInput(attrs={'class': 'superuser-checkbox'}),
            'is_mentor': forms.CheckboxInput(attrs={'class': 'mentor-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'staff-checkbox'}),
            'wallet': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_student': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
            # 'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'user_permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
            }
