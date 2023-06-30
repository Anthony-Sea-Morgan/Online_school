from rest_framework import generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.response import Response
from mainpage.models import Course
from .serializers import CourseSerializer


class ChatMessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CourseListView(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'
