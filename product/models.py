from django.db import models
from core.models import BaseModel

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name