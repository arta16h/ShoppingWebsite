from .models import Product, Category
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ProductListView(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)