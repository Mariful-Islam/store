from django.urls import path
from rest_framework.routers import DefaultRouter
from store.order.api.views import OrderModelViewSet

router = DefaultRouter()

router.register(r'orders', OrderModelViewSet)

urlpatterns = router.urls

