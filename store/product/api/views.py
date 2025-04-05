from rest_framework import generics, viewsets
from store.product.api.serializers import ProductSerializer, ProductDetailSerializer, ProductVariantSerializer, ProductVariantCreateSerializer
from store.product.models import Product, ProductVariant
from store.pagination import StorePagination

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = StorePagination
    lookup_field = 'slug'

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
            print('vvvvvvvvvvvv')
            return ProductVariantCreateSerializer
        return ProductVariantSerializer

    