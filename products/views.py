from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from products.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from products.paginations import DefaultPagination
from rest_framework.permissions import *
from api.permissions import *
from .permissions import *


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["name", "description"]
    ordering_fields = ["price", "updated_at"]
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response(
                {"message": "Product with stock more than 10 could not be deleted"}
            )
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products"))


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get("product_pk"))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get("product_pk"))
