from django.urls import path
from .views import ProductDetailView, ProductListApiView, SearchProductView

urlpatterns = [
    path("products/<slug:slug>", ProductListApiView.as_view()),
    path("product/<slug:slug>", ProductDetailView.as_view()),
    path("search", SearchProductView.as_view()),
]