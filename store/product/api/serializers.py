from rest_framework import serializers
from store.product.models import Product, ProductVariant
import json
from decimal import Decimal


class ProductSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'image',
            'slug',
            'category',
            'total_stock',
            'discount'
        ]

    def get_total_stock(self, obj):
        stock = 0
        for variant in obj.variants.all():
            stock += variant.stock
        return stock
    
    def get_discount(self, obj):
        if obj.discount.all():
            associated_discount = obj.discount.all()[0]
            
            return {
                    'name': associated_discount.name,
                    'type': associated_discount.type,
                    'discount': associated_discount.discount_amount
                }
        else:
            return None    

    


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
        

class ProductWithVariantSerializer(serializers.ModelSerializer):
    # variants = ProductVariantSerializer(many=True)
    variants = serializers.SerializerMethodField()

    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'image',
            'slug',
            'category',
            'discount',
            'variants'
        ]

    def get_discount(self, obj):
        if obj.discount.all():
            associated_discount = obj.discount.all()[0]
            
            return {
                    'name': associated_discount.name,
                    'type': associated_discount.type,
                    'discount': associated_discount.discount_amount
                }
        else:
            return None   

    def get_variants(self, obj):
        variants = obj.variants.all()
        discount = obj.discount.all()[0] if obj.discount.exists() else None
        serialize_variant = []

        for variant in variants:

            discount_price = None

            if discount:
                if discount.type == 'PERCENTAGE':
                    discount_price = Decimal(variant.price) - (Decimal(variant.price)*(discount.discount_amount/100))
                
                elif discount.type == 'FIXED':
                    discount_price = Decimal(variant.price) - Decimal(discount.discount_amount)

                serialize_variant.append({
                    'id': variant.id,
                    'name': variant.name,
                    'sku': variant.sku,
                    'created_at': variant.created_at,
                    'updated_at': variant.updated_at,
                    'price': variant.price,
                    'discount_price': discount_price,
                    'stock': variant.stock,
                    'attribute': variant.attribute,
                    'product': variant.product.id

                })

            else:                
                serialize_variant.append({
                    'id': variant.id,
                    'name': variant.name,
                    'sku': variant.sku,
                    'created_at': variant.created_at,
                    'updated_at': variant.updated_at,
                    'price': variant.price,
                    'discount_price': variant.price if discount_price is None else None ,
                    'stock': variant.stock,
                    'attribute': variant.attribute,
                    'product': variant.product.id

                })
        
        return serialize_variant

    