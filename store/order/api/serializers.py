from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404


from store.order.models import Order, OrderItem
from store.product.models import ProductVariant, Product
from store.user.models import User
from store.payment.models import Payment
from store.user.api.serializers import CustomerSerializer, RetailerSerializer
from store.payment.api.serializers import PaymentSerializer
from store.product.api.serializers import ProductVariantSerializer
import json




class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.SerializerMethodField()
    retailer_name = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'retailer',
            'total_price',
            'total_qty',
            'created_at',
            'updated_at',
            'customer_name',
            'retailer_name',
            'payments',
            'payment_status'
            
        ]

    def get_customer_name(self, obj):
        if obj.customer.first_name:
            return f"{obj.customer.first_name} {obj.customer.last_name}" 
        else:
            return f"{obj.customer.username}"
        
    def get_retailer_name(self, obj):
        if obj.retailer.first_name:
            return f"{obj.retailer.first_name} {obj.retailer.last_name}" 
        else:
            return f"{obj.retailer.username}"
        
    def get_payment_status(self, obj):
        payment_amount = 0

        if obj.payments.all():
            for payment in obj.payments.all():
                payment_amount += float(payment.amount)

        return float(payment_amount) - float(obj.total_price)
    


class OrderCreateSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(write_only=True)
    retailer_name = serializers.CharField(write_only=True)
    variant_payload = serializers.ListField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'created_at',
            'updated_at',
            'customer_name',
            'retailer_name',
            'variant_payload',
        ]

    def create(self, validated_data):
        # Extract the fields from validated_data
        variant_payload = validated_data.pop('variant_payload', [])
        customer_name = validated_data.get('customer_name', '')
        retailer_name = validated_data.get('retailer_name', '')

        total_price = 0
        total_qty = 0

        customer, created = User.objects.get_or_create(
            username=customer_name, 
            defaults={'role': 'CUSTOMER'}
        )

        retailer, created = User.objects.get_or_create(
            username=retailer_name, 
            defaults={'role': 'RETAILER'}
        )

 
        order = Order.objects.create(
            customer=customer,
            retailer=retailer,
            total_price=total_price,
            total_qty=total_qty
        )

     

        for variant in variant_payload:

            # ordered_variant = ProductVariant.objects.get(id=variant['id'])

            ordered_variant = get_object_or_404(ProductVariant, id=variant['id'])
            
            if int(ordered_variant.stock) >= int(variant['quantity']):
                total_price += float(variant['price']) * float(variant['quantity'])
                total_qty += int(variant['quantity'])

                
                ordered_variant.stock -= int(variant['quantity'])
                ordered_variant.save()

                variant_instance = ProductVariant.objects.get(id = variant['id'])

                order_item = OrderItem.objects.create(
                    order=order, 
                    product_variant=variant_instance,
                    quantity=variant['quantity'],
                    price=variant['price'],
                )

                order_item.save()
            
            else:
                raise serializers.ValidationError(
                    "Out of stock"
                )
                
        order.total_price = total_price
        order.total_qty = total_qty
        order.save()

        return order


class OrderDetailSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer(read_only=True)
    retailer = RetailerSerializer(read_only=True)
    variants = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, read_only=True)
    payment_status = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'retailer',
            'total_price',
            'created_at',
            'updated_at',
            'variants',
            'total_qty',
            'payments',
            'payment_status'
        ]

    def get_variants(self, obj):
        variant_list = []

        for item in obj.items.all():
            variant_list.append({
                    "id": item.id,
                    "name": item.product_variant.name,
                    "unit_price": item.price/item.quantity,
                    "quantity": item.quantity,
                    "price": item.price,
                })
            
        return variant_list

    def get_payment_status(self, obj):
        payment_amount = 0

        if obj.payments.all():
            for payment in obj.payments.all():
                payment_amount += float(payment.amount)

        return float(payment_amount) - float(obj.total_price)