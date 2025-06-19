from django.contrib import admin
from store.category.models import Category, SubCategory, SubSubCategory
# Register your models here.


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)