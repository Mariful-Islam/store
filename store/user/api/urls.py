from django.urls import path
from rest_framework.routers import DefaultRouter
from store.user.api.views import CustomerView, RetailerView

router = DefaultRouter()

router.register(r'customers', CustomerView, basename='customers')
router.register(r'retailers', RetailerView, basename='retailers')


urlpatterns = router.urls