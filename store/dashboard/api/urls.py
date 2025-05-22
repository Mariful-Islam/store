from django.urls import path
from store.dashboard.api.views import dashboardAPI, SalesGraphView

urlpatterns = [
    path('dashboard/', dashboardAPI, name='dashboard-api'),
    path('sales/', SalesGraphView.as_view())
]

