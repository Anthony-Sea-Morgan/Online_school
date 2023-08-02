from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path
import registration.views

from .views import index, CourseDetailView, purchase_confirmation, courses_list, attendance_table, personal_cabinet, course_lessons, about_us_view, not_found

from registration.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', index, name='index'),
    path('courses/', courses_list, name='courses_list'), # В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    path('api/v1/', include('restapi.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('about/', about_us_view, name='about_us'),
    path('course/<int:course_id>/lessons/', course_lessons, name='course_lessons'),
    path('<int:pk>', CourseDetailView.as_view(), name='course_detail'),
    path('attendance/', attendance_table, name='attendance_table'),
    path('not_found/', not_found, name='not_found'),
    path('purchase_confirmation/<int:pk>/', purchase_confirmation, name='purchase_confirmation'),
]
