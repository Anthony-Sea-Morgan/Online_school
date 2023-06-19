from rest_framework import serializers
from mainpage.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'mentor', 'start_date', 'lessons_count']
