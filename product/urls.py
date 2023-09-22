from django.urls import path
from . import views

urlpatterns = [
    path('products/<slug:slug>', views.ProductListView.as_view()),
    path('product/<slug:slug>', views.ProductDetailView.as_view()),
]