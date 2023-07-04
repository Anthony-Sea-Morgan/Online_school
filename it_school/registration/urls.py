from django.urls import include, path, re_path
from . import views
from djoser import views as djoser_views
from djoser import urls as djoser_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', views.login_view, name='login_view'),
    path('register_view/', views.register_view, name='register_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
]
