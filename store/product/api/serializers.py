from rest_framework import serializers
from store.product.models import Product, ProductVariant

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
                    'id',
                    'name',
                    'description',
                    'image',
                    'slug',
                    'category',
                    'variants'
                ]