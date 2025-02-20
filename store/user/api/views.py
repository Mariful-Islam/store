from rest_framework import generics, views
from store.user.models import User
from store.user.api.serializers import CustomerSerializer, RetailerSerializer
from store.pagination import StorePagination


class CustomerListView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = User.objects.filter(role='CUSTOMER')
    pagination_class = StorePagination

class RetailerListView(generics.ListCreateAPIView):
    serializer_class = RetailerSerializer
    queryset = User.objects.filter(role='RETAILER')
    pagination_class = StorePagination