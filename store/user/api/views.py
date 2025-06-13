from rest_framework import generics, viewsets
from store.user.models import User
from store.user.api.serializers import CustomerSerializer, CustomerDetailSerializer, RetailerSerializer, RetailerDetailSerializer
from store.pagination import StorePagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filter


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = User.objects.filter(role='CUSTOMER')
    pagination_class = StorePagination
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter, drf_filter.OrderingFilter)
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['first_name', 'email']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerSerializer
        elif self.action == 'retrieve':
            return CustomerDetailSerializer
        else:
            return CustomerSerializer


class RetailerView(viewsets.ModelViewSet):
    serializer_class = RetailerSerializer
    queryset = User.objects.filter(role='RETAILER')
    pagination_class = StorePagination
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend, drf_filter.SearchFilter, drf_filter.OrderingFilter)
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['first_name', 'email']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RetailerSerializer
        elif self.action == 'retrieve':
            return RetailerDetailSerializer
        else:
            return RetailerSerializer
        


class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=201)