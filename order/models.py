from django.db import models
from django.db.models import Sum, F
from django.db import models

from user.models import User
from user.models import User
from product.models import Product
from user.models import PHONE_REGEX_PATTERN

import pytz
from datetime import datetime
from decimal import Decimal

# Create your models here.

class Discount:
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.discount
    

class Payment:
    is_paid = models.BooleanField()

    def __str__(self):
        return self.is_paid
    

class Order:
    class StatusChoice(models.IntegerChoices):
        PENDING = 1, "PENDING"
        CONFIRMED = 2, "CONFIRMED"
        CANCEL = 3, "CANCELED"

    status = models.IntegerField(choices=StatusChoice.choices, default=1)
    customer = models.ForeignKey("User", on_delete=models.CASCADE)
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE)
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE)

    def __str__(self):
        return f"order id:{self.id}"


class OrderItem:
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)


class Cart:
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    discount = models.OneToOneField("Discount", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "carts"

    def __str__(self):
        return f"user{self.user.id} {self.user.username}"
    
    @property
    def final_price_without_shipping(self):
        cart_items = self.cart_items.select_related("product")
        total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)
        if (
            self.discount
            and self.discount.is_active
            and self.discount.end_time > datetime.now().replace(tzinfo=pytz.utc)
        ):
            return total_price * Decimal(str(1 - self.discount / 100))
        return total_price
    
    @property
    def total_price_with_discount(self):
        cart_items = self.cart_items.select_related("product")
        return sum(item.product.discounted_price * item.quantity for item in cart_items)
    
    @property
    def total_price(self):
        cart_items = self.cart_items.select_related("product")
        return cart_items.aggregate(
            total_price=Sum(F("product__price") * F("quantity")))["total_price"]
    

class CartItem:
    product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        related_name="cart_items",
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart}, {self.product}"

    class Meta:
        verbose_name_plural = "cart items"
        unique_together = ["cart", "product"]