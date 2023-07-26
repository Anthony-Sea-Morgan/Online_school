from django.urls import path
from .views import CourseListViewAPI, CourseDetailViewAPI, PersonalCabinetView, CourseLessonsListView,LessonDetailViewAPI

from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'courses', CourseListViewAPI, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', CourseDetailViewAPI.as_view(), name='info-courses'),
    path('personal_cabinet/', PersonalCabinetView.as_view(), name='personal-cabinet'),
    path('courses/<int:course_id>/lessons/', CourseLessonsListView.as_view(), name='course-lessons-list'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', LessonDetailViewAPI.as_view(), name='info-lessons'),



]
