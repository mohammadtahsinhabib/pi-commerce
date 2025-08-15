from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.filters import ProductFilter
from product.models import Category, Product, ProductReview
from product.paginations import CustomPagination

from .serializers import (CategorySerializer, ProductReviewSerializer,
                          ProductSerializer)


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["price", "created_at"]
    filterset_class = ProductFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.stock > 10:
            return Response(
                {"error": "Cannot delete product with stock greater than 10."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_pk")
        return context
