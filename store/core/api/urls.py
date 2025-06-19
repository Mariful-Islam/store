from django.urls import path
from store.core.api.views import StoreCreateView

urlpatterns = [
    path('store/', StoreCreateView.as_view(), name='dashboard-api')
]

