from django.urls import path
from store.discount.api.views import DiscountModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('discounts', DiscountModelViewSet)



urlpatterns = router.urls
