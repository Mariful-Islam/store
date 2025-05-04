from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.db.models import Sum, Avg, Min, Max, Count

from store.product.models import Product, ProductVariant
from store.order.models import Order, OrderItem
from store.user.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth



now = timezone.now()
today = now.date()
start_of_week = today - timedelta(days=today.weekday())
start_of_month = today.replace(day=1)
three_months_ago = today - timedelta(days=90)
six_months_ago = today - timedelta(days=180)
one_year_age = today - timedelta(days=365)




@api_view(['GET'])
def dashboardAPI(request):

    total_product = Product.objects.all().count()
    total_variant = ProductVariant.objects.all().count()
    stock = ProductVariant.objects.aggregate(sum = Sum('stock'))
    order = Order.objects.aggregate(total_order_qty = Sum('total_qty'), total_order_price = Sum('total_price'))
    totol_order = Order.objects.all().count()
    customers = User.objects.filter(role='CUSTOMER').count()
    retailers = User.objects.filter(role='RETAILER').count()



    daily = Order.objects.filter(created_at__gte=today - timedelta(days=30)).annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    
    weekly = Order.objects.filter(created_at__gte=today - timedelta(weeks=12)).annotate(
        week=TruncWeek('created_at')
    ).values('week').annotate(total_sales=Sum('total_price')).order_by('week')

    monthly = Order.objects.filter(created_at__gte=today - timedelta(days=365)).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(total_sales=Sum('total_price')).order_by('month')
    

    # Aggregate total quantity sold for each product variant
    product_sales = (
        OrderItem.objects
        .values('product_variant')  # Group by product_variant
        .annotate(total_quantity_sold=Sum('quantity'))  # Sum of quantities
        .order_by('-total_quantity_sold')  # Sort from highest to lowest
    )

    # Fetch product details and return
    top_selling_products = []
    for item in product_sales:
        try:
            variant = ProductVariant.objects.get(id=item['product_variant'])
            top_selling_products.append({
                'variant_id': variant.id,
                'sku': variant.sku,
                'name': str(variant),  # Assumes __str__ is defined in ProductVariant
                'total_quantity_sold': item['total_quantity_sold'],
                'total_sold_amount': item['total_quantity_sold'] * variant.price,
                'price': variant.price,
                'stock': variant.stock
            })
        except ProductVariant.DoesNotExist:
            continue

    


    
    data = {
        "total_product": total_product,
        "total_variant": total_variant,
        "stock": stock['sum'],
        "totol_order": totol_order,
        "total_order_qty": order['total_order_qty'],
        "total_order_price": order['total_order_price'],
        "customers": customers,
        "retailers": retailers,
        "sells": {"daily": daily, "weekly": weekly, "monthly": monthly},
        "top_selling_products": top_selling_products

    }

    return Response(data, status=status.HTTP_200_OK)