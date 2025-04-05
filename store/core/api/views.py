from rest_framework import generics


from store.core.models import StoreInfo
from store.core.api.serializers import StoreInfoSerializer



class StoreCreateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = StoreInfoSerializer
    queryset = StoreInfo.objects.all()

