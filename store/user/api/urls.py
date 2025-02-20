from django.urls import path
from store.user.api.views import CustomerListView, RetailerListView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer-list-create'),
    path('retailers/', RetailerListView.as_view(), name='retailer-list-create')
]
