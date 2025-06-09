from django.db import models
from store.product.models import Product
from store.core.models import AbstactDateTime




class Discount(AbstactDateTime):

    TYPE_CHOICE = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed')
    ]

    name = models.CharField(max_length=500)
    products = models.ManyToManyField(Product, related_name='discount')
    type = models.CharField(choices=TYPE_CHOICE, max_length=100)
    discount_amount=models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.name} - {self.type} - {self.discount_amount}"