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
            'address',
            'role'
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


            retailers_order.append({
                "id": order.id,
                "customer_name": customer_name,
                "total_price": order.total_price,
                "total_qty": order.total_qty
            })

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
            'address',
            'role'
        ]


class CustomerDetailSerializer(RetailerDetailSerializer):
  
  def get_orders(self, obj):
        customers_order = []

        for order in obj.orders_customer.all():

            retailer_name = ''
            if order.customer.first_name:  # CustomerDetail shows retailer info instead of customer
                retailer_name = f"{order.customer.first_name} {order.customer.last_name}-{order.customer.username}"
            else:
                retailer_name = order.customer.username

            customers_order.append({
                "id": order.id,
                "retailer_name": retailer_name,  # Showing retailer info for CustomerDetail
                "total_price": order.total_price,
                "total_qty": order.total_qty
            })

        return customers_order