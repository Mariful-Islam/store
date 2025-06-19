"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create the schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Store",
      default_version='v1',
      description="Store api description ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='home'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    
    # Optional: ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),


    path('store/product/api/', include('store.product.api.urls')),
    path('store/order/api/', include('store.order.api.urls')),
    path('store/user/api/', include('store.user.api.urls')),
    path('store/payment/api/', include('store.payment.api.urls')),
    path('store/dashboard/api/', include('store.dashboard.api.urls')),
    path('store/discount/api/', include('store.discount.api.urls')),
    path('store/category/api/', include('store.category.api.urls')),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

