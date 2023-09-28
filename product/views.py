from .models import Product, Category
from .serializers import ProductSerializer, SearchProductSerializer, ProductListSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ProductListApiView(APIView):
    def get(self, request):
        search = request.GET.get("search")
        if not search:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(title__icontains = search)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

# class ProductListView(APIView):
#     def get(self, request, slug):
#         category = Category.objects.get(slug=slug)
#         products = Product.objects.filter(category=category)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    

class ProductDetailView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class SearchProductView(APIView):
    def post(self, request):
        serializer=SearchProductSerializer(data=request.data)
        if serializer.is_valid():
            products=Product.objects.filter(name__contains= serializer.data.get("name"))
            if products:
                serializer = ProductListSerializer(products, many=True)
                return Response(serializer.data)
            return Response (status=status.HTTP_404_NOT_FOUND)