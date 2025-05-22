from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Min, Max, Count

from store.product.models import Product, ProductVariant
from store.order.models import Order, OrderItem
from store.user.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
from django.db.models.functions import TruncDate


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


    orders_by_hour = (
        Order.objects
        .filter(created_at__date=today)
        .annotate(hour=TruncHour('created_at'))
        .values('hour')
        .annotate(total_sales=Sum('total_price'))
        .order_by('hour')
    )


    hourly_sells_result = []
    for entry in orders_by_hour:
        formatted_time = entry['hour'].strftime("%I:00%p")
        hourly_sells_result.append({
            "label": formatted_time,
            "total_sales": float(entry['total_sales'])
        })
    


    orders_by_daily = Order.objects.filter(created_at__gte=today - timedelta(days=30)).annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    
    daily_sells_result = []
    for entry in orders_by_daily:
        formatted_time = entry['day'].strftime("%d %b")
        daily_sells_result.append({
            "label": formatted_time,
            "total_sales": float(entry['total_sales'])
        })




    orders_by_monthly = Order.objects.filter(
        created_at__gte=today - timedelta(days=365)
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_sales=Sum('total_price')
    ).order_by('month')

    # Format the result for use (e.g., for charts)
    monthly_sells_result = []
    for entry in orders_by_monthly:
        formatted_time = entry['month'].strftime("%b")  # e.g., "Jan", "Feb"
        monthly_sells_result.append({
            "label": formatted_time,
            "total_sales": float(entry['total_sales'])  # Convert Decimal to float for JSON or frontend use
        })


    # Aggregate total quantity sold for each product variant
    product_sales = (
        OrderItem.objects
        .values('product_variant')  # Group by product_variant
        .annotate(total_quantity_sold=Sum('quantity'))  # Sum of quantities
        .order_by('-total_quantity_sold')  # Sort from highest to lowest
    )

    # Fetch product details and return
    top_selling_products = []
    for item in product_sales[0: 12]:
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
        "sells": {"hourly" : hourly_sells_result, "daily": daily_sells_result, "monthly": monthly_sells_result},
        "top_selling_products": top_selling_products

    }

    return Response(data, status=status.HTTP_200_OK)




class SalesGraphView(APIView):
    def get(self, request):
        # Range selector (default to last 7 days)
        range_param = request.GET.get("range", "last_7_days")
        current_time = now

        time_ranges = {
            "today": current_time.replace(hour=0, minute=0, second=0),
            "yesterday": current_time - timedelta(days=1),
            "last_7_days": current_time - timedelta(days=7),
            "last_10_days": current_time - timedelta(days=10),
            "last_1_month": current_time - timedelta(days=30),
            "last_6_months": current_time - timedelta(days=182),
            "last_1_year": current_time - timedelta(days=365),
        }

        start_time = time_ranges.get(range_param, current_time - timedelta(days=7))

        # Group sales by day and sum
        sales_data = (
            Order.objects.filter(created_at__gte=start_time)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(total_sales=Sum('total_price'))
            .order_by('date')
        )

        # Prepare graph data
        x_data = [entry['date'].strftime("%Y-%m-%d") for entry in sales_data]
        y_data = [float(entry['total_sales']) for entry in sales_data]

        return Response({
            "x": x_data,
            "y": y_data,
            "label": f"Sales from {start_time.date()} to {current_time.date()}"
        })