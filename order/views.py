from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from .serializers import AddtoCartSerializer

# Create your views here.

class AddtoCartApiView(APIView) :
    def get (self, request) :
        serializer = AddtoCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            print(serializer.data)

def delete_cart(request, response) -> None:
    if request.COOKIES.get("cart"):
        response.delete_cookie("cart")

class DeleteCartView(View):
    def get(self, request, *args, **kwargs):
        response = redirect(self.success_redirect_url)
        delete_cart(request, response)
        response.delete_cookie("cart")