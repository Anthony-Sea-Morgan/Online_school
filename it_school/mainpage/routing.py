from django.urls import re_path
from .consumers import CustomConsumer

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<group_id>\d+)/$', CustomConsumer.as_asgi()),
    # Другие URL-шаблоны WebSocket...
]