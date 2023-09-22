from django.shortcuts import render
from .serializers import AddtoCartSerializer

# Create your views here.

class AddtoCartApiView(ApiView) :
    def get (self, request) :
        serializer = AddtoCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            print(serializer.data)