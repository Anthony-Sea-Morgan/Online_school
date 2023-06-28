from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path
import registration.views
from . import views
from registration.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),# В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    path('api/', include('restapi.urls')),
    path('<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
]
