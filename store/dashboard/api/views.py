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
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth, TruncYear, TruncDate
from django.utils.dateparse import parse_date
from rest_framework import generics
import datetime
from store.dashboard.api.serializers import SellsSerializer
from django.db.models.functions import ExtractHour
import math
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from datetime import datetime
from django.utils.timezone import make_aware
from calendar import monthrange

today = datetime.today()

class CounterAPIView(APIView):

    def get(self, request):

        today = timezone.now().date()
        default_start = today - timedelta(days=30)

        order_items = OrderItem.objects.select_related('order').filter(
            order__created_at__date=today,
        )

        product_count = Product.objects.count()
        variant_count = ProductVariant.objects.count()
        stock_count = ProductVariant.objects.aggregate(sum = Sum('stock'))
        
        customer_count = User.objects.filter(role='CUSTOMER').count()
        total_sales = order_items.aggregate(revenue=Sum('price'))['revenue'] or 0


        total_orders = Order.objects.filter(
                created_at__date=today).count()
        

        return Response({
            'product_count': product_count,
            'total_variant': variant_count,
            'stock': stock_count['sum'],
            'customers': customer_count,
            'total_sales': total_sales,
            'total_orders': total_orders,
           
        })



class SalesView(APIView):
    def get(self, request):

        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        date_str = request.query_params.get('date')

        month_str = request.query_params.get('month')


        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            date_diff = (start_date-end_date).days 

            sales_data = Order.objects.filter(
                                            created_at__gte=end_date.date(), 
                                            created_at__lte=start_date.date()
                                        )


            if date_diff <= 30:
                sales_data_day = sales_data.annotate(date = TruncDate('created_at')).values('date').annotate(total_sales=Sum('total_price')).order_by('date')

                sales_by_day = {}

                for i in reversed(range(int(date_diff))):
                    label = today - timedelta(days=i)
         
                    sales_by_day[label.strftime('%d %B %Y')] = 0


                for entry in sales_data_day:
                    label = entry['date'].strftime('%d %B %Y')
           
                    sales_by_day[label] = entry['total_sales']
                
                return Response(sales_by_day)

            else:
                sales_data_monthly = sales_data.annotate(month = TruncMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by('month')

                sales_by_month = {}
                month = math.floor(date_diff/30)

                for i in reversed(range(month)):
                    label_date = today - relativedelta(months=i)  # Get previous i-th month
                    label = label_date.strftime('%b %Y')  # Format as 'YYYY-MM'
                    sales_by_month[label] = 0


                for entry in sales_data_monthly:
                    label = entry['month'].strftime('%b %Y')
           
                    sales_by_month[label] = entry['total_sales']
                
                return Response(sales_by_month)
            

        elif month_str:

            month = datetime.strptime(month_str, '%Y-%m')
            
            start_of_month = make_aware(month)
            
            if month.month == 12:
                end_of_month = make_aware(datetime(month.year + 1, 1, 1)) - timedelta(seconds=1)
            else:
                end_of_month = make_aware(datetime(month.year, month.month + 1, 1)) - timedelta(seconds=1)

            # Filter orders
            sales_data_per_month = Order.objects.filter(
                created_at__gte=start_of_month,
                created_at__lte=end_of_month
            )

            sales_data_per_month_json = sales_data_per_month.annotate(date=TruncDate('created_at')).values('date').annotate(total_sales=Sum('total_price')).order_by('date')

            last_day = monthrange(month.year, month.month)[1]

            sales_by_selected_month = {}

            for day in range(1, last_day + 1):
                label = datetime(month.year, month.month, day)
                sales_by_selected_month[label.strftime('%d %B %Y')] = 0


            for entry in sales_data_per_month_json:
                label = entry['date'].strftime('%d %B %Y')
        
                sales_by_selected_month[label] = entry['total_sales']
            


            return Response(sales_by_selected_month)

        else:
            # Get selected date or use today
            if date_str:
                try:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
            else:
                selected_date = today.date()

           
            
            # Filter orders for that date
            orders = Order.objects.filter(created_at__date=selected_date)

            # Group orders by hour and sum total_price
            hourly_sales = (
                orders.annotate(hour=ExtractHour('created_at'))
                .values('hour')
                .annotate(total_sales=Sum('total_price'))
                .order_by('hour')
            )

            # Build sales dictionary with AM/PM hour labels
            sales_by_hour = {}

            # Initialize all 24 hours with 0
            for h in range(24):
                label = datetime.strptime(str(h), "%H").strftime("%I %p")
                sales_by_hour[label] = 0

            # Fill in actual sales
            for entry in hourly_sales:
                label = datetime.strptime(str(entry['hour']), "%H").strftime("%I %p")
                sales_by_hour[label] = entry['total_sales']

            return Response(sales_by_hour)



class TopSellingProducts(APIView):
    def get(self, request):

        top_selling_variants = []
        

        top_variants = (
            OrderItem.objects
            .values('product_variant')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
        )

        # Enrich with actual ProductVariant instances (optional)
        variant_ids = [item['product_variant'] for item in top_variants]
        variants = ProductVariant.objects.in_bulk(variant_ids)

        # Example output
        for item in top_variants[0:10]:
            variant = variants.get(item['product_variant'])
            if variant:
                top_selling_variants.append({'id': variant.id, 'product_variant': variant.name, 'price': variant.price, 'stock': variant.stock, 'total_quantity': item['total_quantity']})


        return Response(top_selling_variants)


class TopCustomer(APIView):
    def get(self, request):


        orders = Order.objects.values('customer').annotate(total_spend=Sum('total_price')).order_by('-total_spend')

        customer_ids = [order['customer'] for order in orders]
        customers = User.objects.in_bulk(customer_ids)


        top_customers = []
        
        for item in orders[0:10]:
            customer = customers.get(item['customer'])
            if customer:
                top_customers.append({
                    'id': customer.id, 
                    'name': f"{customer.first_name} {customer.last_name}", 
                    "phone": customer.phone, 
                    "total_spend": item['total_spend'] 
                })
            
        return Response(top_customers)
    


class TopRetailer(APIView):
    def get(self, request):

        orders = Order.objects.values('retailer').annotate(total_sold=Sum('total_price')).order_by('-total_sold')

        retailer_ids = [order['retailer'] for order in orders]
        retailers = User.objects.in_bulk(retailer_ids)

        top_retailers = []
        
        for item in orders[0:10]:
            retailer = retailers.get(item['retailer'])
            if retailer:
                top_retailers.append({
                    'id': retailer.id, 
                    'name': f"{retailer.first_name} {retailer.last_name}", 
                    "phone": retailer.phone, 
                    "total_sold": item['total_sold'] 
                })
            
        return Response(top_retailers)