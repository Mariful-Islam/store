from rest_framework.serializers import ModelSerializer
from store.order.models import Order



class SellsSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'created_at'
        ]