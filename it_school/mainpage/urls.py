from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path

import registration.views
from registration.views import RegistrationView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    # path('register_view', views.register_view, name='register_view'),
    # path('logout_view/', views.logout_view, name='logout_view'),
    # path('admin/', views.dom, name='home'),
    #path('registration', registration.views.RegistrationView, name='register_view'),

]
