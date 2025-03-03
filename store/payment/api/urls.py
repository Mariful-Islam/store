from django.urls import path
from store.payment.api.views import MakePaymentByOrder

urlpatterns = [
    path('payments/', MakePaymentByOrder.as_view(), name='make-payment')
]
