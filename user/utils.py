import datetime, jwt
from django.conf import settings
from rest_framework.views import Response
from datetime import timedelta, datetime

class JwtHelper:
    @staticmethod
    def generate_jwt_token(user_id, secret_key, expires_in_minutes):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

def generate_access_token(user, expiration_time_minutes=60):
    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=0, minutes=expiration_time_minutes),
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token


def generate_refresh_token(user, expiration_time_days=7):
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=expiration_time_days),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256")
    return refresh_token