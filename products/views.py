from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from products.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from products.paginations import DefaultPagination

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


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