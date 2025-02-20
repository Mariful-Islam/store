from django.db import models
from store.core.models import AbstactDateTime
# Create your models here.


class Product(AbstactDateTime):
    name = models.CharField(max_length=255,)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    slug = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name



class ProductVariant(AbstactDateTime):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    attribute = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.product.name} - {self.name} - {self.sku}'