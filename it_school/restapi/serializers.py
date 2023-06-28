from rest_framework import serializers


from mainpage.models import Course, DAYS_OF_WEEK_CHOICES
from .models import ChatMessage


class CourseSerializer(serializers.ModelSerializer):
    days_of_week = serializers.MultipleChoiceField(choices=DAYS_OF_WEEK_CHOICES)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        days_of_week = validated_data.pop('days_of_week', [])
        instance = super().create(validated_data)
        instance.days_of_week.set(days_of_week)
        return instance


class ChatMessageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['author']
        extra_kwargs = {
            'text': {'required': False}
        }
