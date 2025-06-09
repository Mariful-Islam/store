from django.db import models
from store.user.models import User
from store.product.models import ProductVariant
from django.utils import timezone
from store.core.models import AbstactDateTime


# Create your models here.
class Order(AbstactDateTime):
    customer = models.ForeignKey(User, related_name='orders_customer', on_delete=models.CASCADE, blank=True, null=True)
    retailer = models.ForeignKey(User, related_name='orders_retailer', on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_qty = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id} by {self.customer.first_name}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the variant at the time of purchase

    def __str__(self):
        return f'{self.quantity} x {self.product_variant.sku} for Order {self.order.id}'



