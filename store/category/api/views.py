from rest_framework import generics, viewsets
from rest_framework.views import APIView
from store.category.models import Category, SubCategory, SubSubCategory
from store.category.api.serializers import CategorySerializer, SubCategorySerializer, SubSubCategorySerializer, CategoryListSerializer, ExtendSubCategorySerializer, ExtendSubSubCategorySerializer
from store.pagination import ShortStorePagination


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    



class SubCategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ExtendSubCategorySerializer
        return SubCategorySerializer



class SubSubCategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = SubSubCategorySerializer
    queryset = SubSubCategory.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ExtendSubSubCategorySerializer
        return SubCategorySerializer



class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    pagination_class = ShortStorePagination