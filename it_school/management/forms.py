from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from mainpage.models import Course
from django import forms




class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'description', 'short_des', 'difficulty', 'rating', 'price', 'mentor', 'start_date','start_time', 'days_of_week']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'description': SummernoteWidget(attrs={'class': 'form-group'}),
            'short_des': forms.Textarea(attrs={'class': 'form-group'}),
            'difficulty': forms.Select(attrs={'class': 'form-group'}),
            'rating': forms.NumberInput(attrs={'class': 'form-group'}),
            'price': forms.NumberInput(attrs={'class': 'form-group'}),
            'mentor': forms.Select(attrs={'class': 'form-group'}),
            'start_date': forms.DateInput(attrs={'class': 'form-group'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-group'}),
            'days_of_week': forms.CheckboxSelectMultiple(attrs={'class': 'form-group', 'style':'width: 25%;height: 100%;'}),
        }