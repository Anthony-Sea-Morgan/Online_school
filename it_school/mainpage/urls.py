from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path
import registration.views
from . import views
from .views import lesson_list
from registration.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),
    # В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    path('register/', registration.views.register_user, name='register'),
    path('login/', registration.views.login_view, name='login'),
    path('logout/', registration.views.LogoutView.as_view(), name='logout'),
    path('api/', include('restapi.urls')),
    path('<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('lessons/', lesson_list, name='lesson_list'),
    path('personal_cabinet/', views.personal_cabinet, name='personal_cabinet'),
]
