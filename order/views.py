from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)

from .models import Cart
from .serializers import CartSerializer


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
