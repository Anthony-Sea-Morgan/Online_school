from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('courses/', views.CourseListView, name='course_list'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('lessons/', views.LessonView.as_view(), name='lesson_view'),
    path('courses/<int:pk>/remove_participant/', views.remove_participant, name='remove_participant'),
    path('courses/<int:pk>/add_participant/', views.add_participant, name='add_participant'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    # path('lesson/update/<int:pk>/', views.lesson_update, name='lesson_update')
]