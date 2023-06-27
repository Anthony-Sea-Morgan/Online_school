from rest_framework import serializers
from mainpage.models import Course
from .models import ChatMessage


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['author']
        extra_kwargs = {
            'text': {'required': False}
        }
