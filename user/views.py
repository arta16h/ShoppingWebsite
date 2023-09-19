import random
from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.views import Response, APIView

from .models import User
from .serializer import UserSerializer,UserVerifySerializer

# Create your views here.

def generate_2fa(request): 
    request.session["2FA"] = random.randint(1000, 9999)
    request.session["2fa_expire"] = (timezone.now() + timedelta(minutes=1)).strftime("%d/%m/%Y, %H:%M:%S")
    print(f"generated:{request.session['2FA']}  exp:{request.session['2fa_expire']}")
    return request  


class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)