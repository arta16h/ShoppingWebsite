from .models import User
import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError


class UserAuthBackend(BaseBackend):

    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header=request.headers.get('Authorization')
        jwt_token = JWTAuthentication.get_the_token_from_header(authorization_header)
        user_id = payload.get('user_id')
        user = User.objects.filter(id=user_id).first()

        if not authorization_header:
            return None
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            raise ParseError()
        
        if not user_id:
            raise AuthenticationFailed('User Id not found in JWT')
        
        if not user:
            raise AuthenticationFailed('User not found')
        
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token     