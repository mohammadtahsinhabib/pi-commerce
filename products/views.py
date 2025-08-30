from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class ProductViewSet(ModelViewSet):

    
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get("category_id")
        if category_id is not None:
            Product.objects.filter(category_id=category_id)
        
        return queryset
        



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



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}