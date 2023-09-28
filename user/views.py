import random, datetime, jwt
from datetime import timedelta

from django.conf import settings
from django.views import View
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import update_last_login

from rest_framework import status, permissions, exceptions
from rest_framework.views import Response, APIView
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializer import UserSerializer, LoginOTPSerializer, LoginSerializer
from .utils import generate_access_token, generate_refresh_token

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
    
class SendOTPView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_otp(request, serializer.data["phone"])
            return Response (data={"message":"200"})


class VerifyOTP(APIView):
    def post(self, request):
        serliazer=LoginOTPSerializer(data=request.data, context={"request":request})
        if serliazer.is_valid(raise_exception=True):
            user=User.objects.get(phone=request.session.get("phone"))
            access_token=user.get_access_token()
            refresh_token=user.get_refresh_token()
            return Response(data={"message":"success", "AT":access_token, "RT":refresh_token})


class LoginView(APIView):

    def post(self, request):
        phone = request.data["phone"]
        password = request.data["password"]
        user = User.objects.filter(phone=phone).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt":token
            }

        update_last_login(None, user)
        return response
    

class UserVerifyAPIView(APIView):

    def get(self, request):
        if (not self.expiration_time) or (
            timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S")):
            request = generate_2fa(request)
        else:
            print(f"otp:{self.generated_otp}  exp:{self.expiration_time}")
        return super().get(request)

    def post(self, request):
        if not all([self.generated_otp,self.expiration_time]):
            return Response("panel:user_verify")
        if timezone.now() > timezone.datetime.strptime(self.expiration_time, "%d/%m/%Y, %H:%M:%S"):
            print("expired")
            self.request = generate_2fa(request)
            form = self.get_form()
            form.add_error("otp", "A new code has been sent to you")
            return self.form_invalid(form)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        entered_otp = form.clean().get("otp")
        if entered_otp == str(self.generated_otp):
            self.request.session.pop("2FA")
            self.request.session.pop("2fa_expire")
            self.request.session["authenticated"] = True
            user = User.objects.get(phone=self.user_phone)
            login(self.request, user, "users.auth.UserAuthBackend")
            self.request.session["phone"] = user.phone
            return super().form_valid(form)
        else:
            form.add_error("otp","Invalid code entered")
            return self.form_invalid(form)
    

class LogoutAPIView(APIView):

    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {"message": "succed"}
        return response
    

class RefreshTokenApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refreshtoken")
        if refresh_token is None:
            raise exceptions.AuthenticationFailed
        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("expired refresh token")

        user = User.objects.filter(id=payload.get("user_id")).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("user isn't active")

        access_token = generate_access_token(user)
        return Response({"access_token": access_token})