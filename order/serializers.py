from rest_framework import serializers
from .models import Order, OrderItem
from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer
from user.serializer import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "user",
            "cart_items",
            "total_price_with_discount",
            "final_price_without_shipping",
            "total_price",
        ]


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
        
        
class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemSerializer(many=True)
    
    class Meta:
        model=Order
        fields=[
            "customer",
            "discount_amount",
            "payment_amount",
            "order_items",
            ]