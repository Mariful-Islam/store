from store.dashboard.consumers import DashboardConsumer, DashboardCardConsumer
from django.urls import path

ws_urlpatters = [
    path('ws/dashboard/', DashboardConsumer.as_asgi()),
    path('ws/dashboard/cards/', DashboardCardConsumer.as_asgi())
]