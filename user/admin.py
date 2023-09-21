from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

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


admin.site.register(User, CustomUserAdmin)