from django.urls import path
from .views import AddtoCartApiView

urlpatterns = [
    path("add", AddtoCartApiView.as_view()),
]