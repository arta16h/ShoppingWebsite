from django.db import models
from core.models import BaseModel

# Create your models here.

class Discount(BaseModel):
    discount = models.IntegerField(max_digits=2, default=0)

    def __str__(self):
        return self.discount