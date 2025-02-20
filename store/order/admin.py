from django.contrib import admin
from store.order.models import Order, OrderItem

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)