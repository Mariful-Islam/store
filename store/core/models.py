from django.db import models

# Create your models here.



class AbstactDateTime(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True




class StoreInfo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo')
