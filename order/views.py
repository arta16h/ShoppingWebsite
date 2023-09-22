from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AddtoCartSerializer

# Create your views here.

class AddtoCartApiView(APIView) :
    def get (self, request) :
        serializer = AddtoCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            print(serializer.data)