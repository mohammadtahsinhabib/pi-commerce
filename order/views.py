from order.services import OrderService
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CreateOrderSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .models import Cart, CartItem
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.models import Order
from order.serializers import OrderSerializer , UpdateOrderSerializer,EmptySerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
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
        if not getattr(self, 'swagger_fake_view', False):
            context["cart_id"] = self.kwargs["cart_pk"]
        # context["cart_id"] = self.kwargs["cart_pk"]
        return context


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete",  "head", "options"]

    def get_serializer_context(self):
        return {"user_id":self.request.user.id,"user": self.request.user}

    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return CreateOrderSerializer
        elif self.request.method in ["PATCH"]:
            return UpdateOrderSerializer
        elif self.request.method in ["Cancel"]:
            return EmptySerializer
        return OrderSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__product").all()

        return Order.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )
    

    @action(detail = True, methods=["post"],permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user = request.user)
        return Response({"message": "Order cancelled successfully."})
    
    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def update_status(self,request,pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Order status updated successfully."})
    
    
