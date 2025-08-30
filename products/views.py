from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListCreateView(ListCreateAPIView):
    """
    GET: List all products
    POST: Create a new product
    """
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a product
    PUT: Update a product
    DELETE: Delete a product
    """
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    lookup_field = "id"


class CategoryListCreateView(ListCreateAPIView):
    """
    GET: List all categories with product counts
    POST: Create a new category
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products"))


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single category with product count
    PUT: Update a category
    DELETE: Delete a category
    """
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products"))
