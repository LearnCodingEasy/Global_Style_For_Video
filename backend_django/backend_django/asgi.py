"""
ASGI config for backend_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')

application = get_asgi_application()
"""


import automation.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application

# 1. تهيئة الإعدادات أولاً
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django_asgi_app = get_asgi_application()

# 2. الاستيراد بعد التهيئة لتجنب AppRegistryNotReady

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            automation.routing.websocket_urlpatterns
        )
    ),
})
