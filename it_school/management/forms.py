from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from mainpage.models import Course, Lesson, CustomGroup
from django.forms import ModelForm, TextInput, Textarea,  ClearableFileInput
from django import forms




class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'description', 'short_des', 'lessons_count', 'difficulty', 'technologies', 'rating', 'price', 'mentor', 'start_date','start_time', 'days_of_week', 'img', 'tech_img',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'description': SummernoteWidget(attrs={'class': 'form-group'}),
            'short_des': forms.Textarea(attrs={'class': 'form-group'}),
            'difficulty': forms.Select(attrs={'class': 'form-group'}),
            'rating': forms.NumberInput(attrs={'class': 'form-group', 'type':'number'}),
            'lessons_count': forms.NumberInput(attrs={'class': 'form-group', 'type':'number'}),
            'price': forms.NumberInput(attrs={'class': 'form-group', 'type':'number'}),
            'mentor': forms.Select(attrs={'class': 'form-group'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group','id': 'id_start_date', 'name': 'start_date', 'type':'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group','id': 'id_start_time', 'name': 'start_time', 'type':'time'}),
            'days_of_week': forms.CheckboxSelectMultiple(attrs={'class': 'form-group', 'style':'width: 25%;height: 100%;'}),
            'technologies': forms.CheckboxSelectMultiple(attrs={'class': 'form-group', 'style':'width: 25%;height: 100%;'}),
            'img': ClearableFileInput(attrs={'class': "file-input",'id': "img",'value': "",}),
            'tech_img': ClearableFileInput(attrs={'class': "file-input",'id': "img_tech",'value': "",}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['mentor_owner', 'title', 'material', 'day_of_week', 'start_date', 'start_time']
        widgets = {
            'mentor_owner': forms.Select(attrs={'class': 'form-group'}),
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'material': SummernoteWidget(attrs={'class': 'form-group'}),
            'day_of_week': forms.Select(attrs={'class': 'form-group'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group', 'type': 'time'}),
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