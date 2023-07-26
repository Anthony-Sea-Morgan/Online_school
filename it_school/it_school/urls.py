"""
URL configuration for it_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from mainpage.views import *
from registration.views import *
from restapi.views import *
from management.views import *
from chat.views import chat_room
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('sDgT6wR7AaZbF4xU9gBcX0hJkL3qPmV6aWnD8eR9dYfU3kK1rN3sP0mCpJ5dG6h/', admin.site.urls),
    path('api/', include('restapi.urls')),
    path('', include('registration.urls')),
    path('management/', include('management.urls')),
    path('', include('mainpage.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('summernote/', include('django_summernote.urls')),
    # path('api/v1/auth/token/login/', djoser_views.TokenCreateView.as_view(), name='token_create'),
    path('chat/', include('chat.urls')),
    re_path(r'^chat/(?P<room_name>\w+)/$', chat_room, name='chat_room'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()