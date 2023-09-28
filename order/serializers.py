from rest_framework import serializers
from .models import Order, OrderItem


class AddtoCartSerializer(serializers.Serializer) :
    product = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=[
            "orders",
            "products",
            "quantity",
            "unit_price",
            "discount_amount",
            ]
        
        
