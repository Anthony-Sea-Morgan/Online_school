from django.urls import include, path
from rest_framework import routers
from .views import CourseViewSet
from .views import ChatMessageListCreateView

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', ChatMessageListCreateView.as_view(), name='chat-messages'),

]
