from django.urls import path
from store.dashboard.api.views import CounterAPIView, SalesView, TopSellingProducts

urlpatterns = [
    path('dashboard/counter/', CounterAPIView.as_view(), name='counter-api'),
    path('dashboard/sales/', SalesView.as_view(), name='sales'),
    path('dashboard/top-selling-variant/', TopSellingProducts.as_view())
]

