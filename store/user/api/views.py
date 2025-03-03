from rest_framework import generics, viewsets
from store.user.models import User
from store.user.api.serializers import CustomerSerializer, CustomerDetailSerializer, RetailerSerializer, RetailerDetailSerializer
from store.pagination import StorePagination




class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = User.objects.filter(role='CUSTOMER')
    pagination_class = StorePagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerSerializer
        elif self.action == 'retrieve':
            return CustomerDetailSerializer
        else:
            return CustomerSerializer


class RetailerView(viewsets.ModelViewSet):
    serializer_class = RetailerSerializer
    queryset = User.objects.filter(role='RETAILER')
    pagination_class = StorePagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RetailerSerializer
        elif self.action == 'retrieve':
            return RetailerDetailSerializer
        else:
            return RetailerSerializer