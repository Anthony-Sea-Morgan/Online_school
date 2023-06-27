from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import ChatMessage
from .serializers import ChatMessageSerializer

# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response

from mainpage.models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def retrieve(self, request, pk=None):
        # Метод retrieve обрабатывает GET-запросы для получения конкретного курса по его идентификатору (pk)
        if pk is None:
            return Response(status=400)
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=404)

        serializer = CourseSerializer(course)
        return Response(serializer.data)


class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
