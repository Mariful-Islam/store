from django.urls import path
from rest_framework.routers import DefaultRouter
from store.user.api.views import CustomerView, RetailerView, Signup
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

router = DefaultRouter()

router.register(r'customers', CustomerView, basename='customers')
router.register(r'retailers', RetailerView, basename='retailers')


urlpatterns = router.urls

urlpatterns += [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verfiy')
]