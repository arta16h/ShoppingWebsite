import random, datetime, jwt
from datetime import timedelta

from django.views import View
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import update_last_login

from rest_framework import status
from rest_framework.views import Response, APIView
from rest_framework.exceptions import AuthenticationFailed

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
    

class LoginView(APIView):

    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']
        user = User.objects.filter(phone=phone).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
            }

        update_last_login(None, user)
        return response
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")