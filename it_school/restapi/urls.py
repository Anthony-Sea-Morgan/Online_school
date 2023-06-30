from django.urls import path
from .views import CourseListView, CourseDetailView
from .views import ChatMessageListCreateView

from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'courses', CourseListView, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='info-courses'),
    path('chat/', ChatMessageListCreateView.as_view(), name='chat-messages'),
]
