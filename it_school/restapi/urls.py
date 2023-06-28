from django.urls import path
from .views import CourseListView, CourseDetailView
from .views import ChatMessageListCreateView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='all-courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='info-courses'),
    path('chat/', ChatMessageListCreateView.as_view(), name='chat-messages'),
]
