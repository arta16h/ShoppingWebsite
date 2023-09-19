from django.db import models
from core.models import BaseModel

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name