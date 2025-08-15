from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Cart, CartItem
from .serializers import *
from rest_framework.viewsets import ModelViewSet


class CartViewSet(CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddItemSerializer
        elif self.request.method in ["PATCH"]:
            return UpdateItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["cart_id"] = self.kwargs["cart_pk"]
        return context
