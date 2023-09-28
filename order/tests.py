from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from product.models import Product, Category
from serializers import CartSerializer
from products.api.serializers import ProductSerializer
from ..models import CartItem, Cart
from model_bakery import baker
from accounts.models import User
from decimal import Decimal

# Create your tests here.
