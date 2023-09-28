from django.urls import path
from .views import (
    LoginView,
    LogoutAPIView,
    VerifyOTP,
    SendOTPView,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("sendotp/", SendOTPView.as_view(), name="sendotp"),
    path("verify/", VerifyOTP.as_view(), name="verify"),
]