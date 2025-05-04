from rest_framework import generics, viewsets
from store.order.api.serializers import OrderSerializer, OrderCreateSerializer, OrderDetailSerializer
from store.order.models import Order
from store.pagination import StorePagination
from rest_framework.response import Response

from django_filters import rest_framework as filters
import django_filters
from rest_framework import filters as drf_filter



class OrderFilter(filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['created_at']

class OrderModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = StorePagination

    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter, drf_filter.OrderingFilter)
    search_fields = ['customer__username', 
                     'customer__first_name', 
                     'customer__last_name', 
                     'customer__email', 
                     'customer__phone',
                     'retailer__username', 
                     'retailer__first_name', 
                     'retailer__last_name', 
                     'retailer__email', 
                     'retailer__phone',

                     ]
    ordering_fields = ['total_price', 'created_at', 'updated_at']
    filterset_class = OrderFilter


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer
        
