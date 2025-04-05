from django.urls import path
from store.dashboard.api.views import dashboardAPI

urlpatterns = [
    path('dashboard/', dashboardAPI, name='dashboard-api')
]

