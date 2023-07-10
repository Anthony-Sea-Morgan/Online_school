from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('courses/', views.CourseListView, name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('lessons/', views.LessonView.as_view(), name='lesson_view'),
]