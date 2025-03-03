from rest_framework import generics
from store.payment.api.serializers import PaymentSerializer
from store.payment.models import Payment


class MakePaymentByOrder(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()