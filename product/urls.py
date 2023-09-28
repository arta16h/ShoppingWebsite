from django.urls import path
from .views import ProductDetailView, ProductListApiView, SearchProductView, ProductCategoryView

urlpatterns = [
    path("products/<slug:slug>", ProductListApiView.as_view()),
    path("product/<slug:slug>", ProductDetailView.as_view()),
    path("search", SearchProductView.as_view()),
    path("podcat/", ProductCategoryView.as_view()),
]