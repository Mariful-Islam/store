from rest_framework.serializers import ModelSerializer
from store.category.models import Category, SubCategory, SubSubCategory



class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'


class SubSubCategorySerializer(ModelSerializer):

    class Meta:
        model = SubSubCategory
        fields = '__all__'




"""
Serializer to extend category, sub category and sub sub category
"""


class ExtendSubSubCategorySerializer(ModelSerializer):

    class Meta:
        model = SubSubCategory
        fields = [
            'id',
            'name',
            'description',


        ]

class ExtendSubCategorySerializer(ModelSerializer):
    sub_sub_category = ExtendSubSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'name',
            'description',
            'sub_sub_category'

        ]

class CategoryListSerializer(ModelSerializer):
    sub_category = ExtendSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
                'id',
                'name',
                'description',
                'sub_category'
            ]