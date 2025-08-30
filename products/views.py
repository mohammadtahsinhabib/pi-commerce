from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(ModelViewSet):
    """
    Supports:
    - GET /products/ → list all products
    - POST /products/ → create a product
    - GET /products/{id}/ → retrieve a product
    - PUT /products/{id}/ → update a product
    - PATCH /products/{id}/ → partial update
    - DELETE /products/{id}/ → delete a product
    """
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    lookup_field = "id"


class CategoryViewSet(ModelViewSet):
    """
    Supports:
    - GET /categories/ → list all categories with product counts
    - POST /categories/ → create a category
    - GET /categories/{id}/ → retrieve a category
    - PUT /categories/{id}/ → update a category
    - PATCH /categories/{id}/ → partial update
    - DELETE /categories/{id}/ → delete a category
    """
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products"))
