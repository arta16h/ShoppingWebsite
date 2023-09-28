from django.db import models

# Create your models here.

class Category:
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class Product:
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name