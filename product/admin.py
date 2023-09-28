from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name", "category")
    list_filter = ("category", "is_available")
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10