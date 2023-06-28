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
from django.urls import include
from mainpage.views import *
from registration.views import *
from restapi.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restapi.urls')),
    path('', include('registration.urls')),
    path('', include('mainpage.urls')),
    path('summernote/', include('django_summernote.urls')),
    # path('api/v1/auth/token/login/', djoser_views.TokenCreateView.as_view(), name='token_create'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

