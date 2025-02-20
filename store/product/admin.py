from django.contrib import admin
from store.product.models import Product, ProductVariant
# Register your models here.


admin.site.register(Product)
admin.site.register(ProductVariant)
