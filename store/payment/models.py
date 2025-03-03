from django.db import models
from store.order.models import Order
# Create your models here.


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), 
                                                             ('Debit Card', 'Debit Card'), 
                                                             ('PayPal', 'PayPal'), 
                                                             ('Bank Transfer', 'Bank Transfer'),
                                                             ('Cash', 'Cash')
                                                            ])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of {self.amount} for Order {self.order.id} via {self.payment_method}'