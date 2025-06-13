from rest_framework import viewsets, generics
from store.discount.models import Discount
from store.discount.api.serializers import DiscountSerializer, DiscountDetailSerializer
from store.pagination import StorePagination
from django_filters import rest_framework as filters
import django_filters
from rest_framework import filters as drf_filter




class DiscountFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    product_name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')

    class Meta:
        model = Discount
        fields = ('name', 'product_name', 'type',)



class DiscountModelViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    pagination_class = StorePagination

    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter, drf_filter.OrderingFilter)
    search_fields = ['name', 'products__name', 'type', 'discount_amount']
    ordering_fields = ['name', 'created_at', 'updated_at', 'discount_amount']
    filterset_class = DiscountFilter

    def get_serializer_class(self):
        
        if self.action == 'retrieve':
            return DiscountDetailSerializer
        else:
            return DiscountSerializer

