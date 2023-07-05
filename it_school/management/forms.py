from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from mainpage.models import Course
from django import forms

class SomeForm(forms.Form):
    description = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['description']
        widgets = {
            'description': SummernoteWidget(),
        }