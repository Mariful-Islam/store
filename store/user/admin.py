from django.contrib import admin
from store.user.models import User
# Register your models here.



class ModelUser(admin.ModelAdmin):

    list_display = ['username']


admin.site.register(User, ModelUser)