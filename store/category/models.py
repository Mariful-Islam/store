from django.db import models
from store.core.models import AbsNameDesc


# Create your models here.
class Category(AbsNameDesc):
    
    def __str__(self):
        return self.name


class SubCategory(AbsNameDesc):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return self.name
    

class SubSubCategory(AbsNameDesc):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_sub_category')

    def __str__(self):
        return self.name