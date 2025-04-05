from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.db.models import Sum, Avg, Min, Max

from store.product.models import Product, ProductVariant
from store.order.models import Order, OrderItem
from store.user.models import User




@api_view(['GET'])
def dashboardAPI(request):

    total_product = Product.objects.all().count()
    total_variant = ProductVariant.objects.all().count()
    stock = ProductVariant.objects.aggregate(sum = Sum('stock'))
    order = Order.objects.aggregate(total_order_qty = Sum('total_qty'), total_order_price = Sum('total_price'))
    totol_order = Order.objects.all().count()
    customers = User.objects.filter(role='CUSTOMER').count()
    retailers = User.objects.filter(role='RETAILER').count()
    
    data = {
        "total_product": total_product,
        "total_variant": total_variant,
        "stock": stock['sum'],
        "totol_order": totol_order,
        "total_order_qty": order['total_order_qty'],
        "total_order_price": order['total_order_price'],
        "customers": customers,
        "retailers": retailers
    }

    return Response(data, status=status.HTTP_200_OK)