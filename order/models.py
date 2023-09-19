from django.db import models
from core.models import BaseModel
from user.models import User

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
    discount = models.ForeignKey(Discount on_delete=models.SET_NULL)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)