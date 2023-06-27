from django.urls import include, path
import registration.views
from . import views

urlpatterns = [
    path('login/', registration.views.login_view, name='login'),
    ]
