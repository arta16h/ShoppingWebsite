from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from rest_framework.views import APIView
from .serializers import AddtoCartSerializer
from .models import OrderItem

# Create your views here.

class AddtoCartApiView(APIView) :
    def get (self, request) :
        serializer = AddtoCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            print(serializer.data)

def delete_cart(request, response) -> None:
    if request.COOKIES.get("cart"):
        response.delete_cookie("cart")

class DeleteCartView(View):
    def get(self, request, *args, **kwargs):
        response = redirect(self.success_redirect_url)
        delete_cart(request, response)
        response.delete_cookie("cart")


class OrderItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs["pk"]
        order_item_id = request.POST.get("orderitem")
        quantity = request.POST.get("quantity")
        order_item = get_object_or_404(OrderItem, pk=int(order_item_id))

        order_item.quantity = int(quantity)
        order_item.save()

        return redirect("order_details", order_id)
    

