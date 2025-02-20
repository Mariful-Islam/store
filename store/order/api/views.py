from rest_framework import generics, viewsets
from store.order.api.serializers import OrderSerializer, OrderCreateSerializer, OrderDetailSerializer
from store.order.models import Order
from store.pagination import StorePagination


class OrderModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = StorePagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            print('hhhhhhhhhh')
            return OrderDetailSerializer
        else:
            return OrderSerializer