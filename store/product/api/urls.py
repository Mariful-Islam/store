from django.urls import path
from rest_framework.routers import DefaultRouter
from store.product.api.views import ProductViewSet, VariantViewSet



router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'product-variants', VariantViewSet)

urlpatterns = router.urls