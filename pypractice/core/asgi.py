# mysite/asgi.py
import os

import django
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from pypractice.core.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pypractice.settings')
django.setup()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
                    #re_path(r'' + '/(?P<channel>[^/]+)/$', ChatConsumer.as_asgi()),
                ]
            )
        ),
    ),
})