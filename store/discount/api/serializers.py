from rest_framework.serializers import ModelSerializer
from store.discount.models import Discount
from store.product.api.serializers import ProductSerializer


class DiscountSerializer(ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'



class DiscountDetailSerializer(ModelSerializer):
    
    products = ProductSerializer(many=True)

    class Meta:
        model = Discount
        fields = [
            'id',
            'name',
            'type',
            'discount_amount',
            'products'
        ]