from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SearchProductSerializer(serializers.Serializer):
    name=serializers.CharField()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            "name",
            "description",
            "price",
            "quantity",
            "image",
            "category"
            ]