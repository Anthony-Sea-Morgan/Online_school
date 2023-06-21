from django.shortcuts import render

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
