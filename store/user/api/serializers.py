from rest_framework import serializers
from store.user.models import User
import json


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
            'address'
        ]


class RetailerDetailSerializer(serializers.ModelSerializer):

    # orders = OrderSerializer(many=True, read_only=True)
    orders = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
            'address',
            'orders'
        ]
    
    def get_orders(self, obj):
        retailers_order = []

        for order in obj.orders_retailer.all():
            customer_name = ''
            if order.customer.first_name:
                customer_name = f"{order.customer.first_name} {order.customer.last_name}"
            else:
                customer_name = order.customer.username

            print(order)

            retailers_order.append({
                "id": order.id,
                "customer_name": customer_name,
                "total_price": order.total_price,
                "total_qty": order.total_qty
            })
        # orders = obj.orders_retailer.all()
        
        # orders = obj.orders_retailer.all()
        # print(orders, "------------------")
        # If there are orders, serialize them, otherwise return an empty list
        # if orders:
        #     return OrderSerializer(orders, many=True, context=self.context).data
        return retailers_order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
            'address'
        ]