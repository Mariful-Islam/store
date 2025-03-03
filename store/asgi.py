"""
ASGI config for store project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path

from store.dashboard.consumers import RealTimeChartConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")

django_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/dashboard/", RealTimeChartConsumer.as_asgi()),
                ]
            )
        ),
    }
)
