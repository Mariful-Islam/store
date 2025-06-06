from store.dashboard.consumers import DashboardConsumer
from django.urls import path

ws_urlpatters = [
    path('ws/dashboard/', DashboardConsumer.as_asgi())
]