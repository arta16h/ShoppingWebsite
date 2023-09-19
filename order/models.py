from django.db import models
from core.models import BaseModel
from user.models import User
from product.models import Product

# Create your models here.

class Discount(BaseModel):
    discount = models.IntegerField(max_digits=2, default=0)

    def __str__(self):
        return self.discount
    

class Payment(BaseModel):
    is_paid = models.BooleanField()

    def __str__(self):
        return self.is_paid
    

class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class OrderItem(BaseModel):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.IntegerField(max_digits=2, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)