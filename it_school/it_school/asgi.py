import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from mainpage.consumers import CustomConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_school.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws', CustomConsumer.as_asgi()),
        ])
    ),
})