from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status",)
    search_fields = ("user",)
    list_filter = ("status",)
    list_editable = ("status",)
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    list_filter = ("product", )
    autocomplete_fields = ("product",)
    list_per_page = 10