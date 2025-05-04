from rest_framework import generics, viewsets
from store.product.api.serializers import (
    ProductSerializer, 
    ProductDetailSerializer, 
    ProductVariantSerializer, 
    ProductVariantCreateSerializer, 
    ProductWithVariantSerializer)
from store.product.models import Product, ProductVariant
from store.pagination import StorePagination, ShortStorePagination
from django_filters import rest_framework as filters
import django_filters
from rest_framework import filters as drf_filter



class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    variant_name = django_filters.CharFilter(field_name='variants__name', lookup_expr='icontains')
    variant_sku = django_filters.CharFilter(field_name='variants__sku', lookup_expr='icontains')
    variant_price = django_filters.CharFilter(field_name='variants__price', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'variant_name', 'variant_sku', 'variant_price')




class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = StorePagination
    lookup_field = 'slug'

    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter, drf_filter.OrderingFilter)
    search_fields = ['name', 'description', 'slug', 'category', 'variants__name']
    ordering_fields = ['name', 'variants__price', 'created_at', 'updated_at']
    filterset_class = ProductFilter


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer



class VariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
    pagination_class = StorePagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method=='POST':
    
            return ProductVariantCreateSerializer
        return ProductVariantSerializer
    
    


class ProductWithVariant(generics.ListAPIView):
    serializer_class = ProductWithVariantSerializer
    queryset = Product.objects.all()
    pagination_class = ShortStorePagination
    
    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter)
    search_fields = ['name', 'description', 'slug', 'category', 'variants__name']
    filterset_class = ProductFilter



    