from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("phone", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")})
        )
    add_fieldsets = (None, {"fields": ("username", "phone", "password", "is_staff", "is_active")})
    search_fields = ("phone")
    ordering = ("first_name","last_name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "street",
    )
    search_fields = ("city","street")
    list_filter = ("city", "street")
    list_per_page = 10


admin.site.register(User, CustomUserAdmin)