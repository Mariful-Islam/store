from django.urls import path
from store.dashboard.api.views import CounterAPIView, SalesView, TopSellingProducts, TopCustomer, TopRetailer

urlpatterns = [
    path('dashboard/counter/', CounterAPIView.as_view(), name='counter-api'),
    path('dashboard/sales/', SalesView.as_view(), name='sales'),
    path('dashboard/top-selling-variant/', TopSellingProducts.as_view()),
    path('dashboard/top-customers/', TopCustomer.as_view()),
    path('dashboard/top-retailers/', TopRetailer.as_view()),

]

