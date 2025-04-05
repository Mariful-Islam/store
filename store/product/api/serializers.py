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
        
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 
                  'name', 
                  'product', 
                  'price',
                  'stock',
                  'attribute'
                ]
    
    def create(self, validated_data):
        name = validated_data['name']
        price = str(validated_data['price'])
        stock = str(validated_data['stock'])
        sku = name + price + stock

        if sku:
            product_variant = ProductVariant.objects.create(
                **validated_data,
                sku=sku
            )

            return product_variant