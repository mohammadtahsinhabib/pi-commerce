from .serializers import ProductImageSerializer
from .models import ProductImage
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from product.filters import ProductFilter
from product.models import Category, Product, ProductReview
from product.paginations import CustomPagination
from .serializers import (
    CategorySerializer,
    ProductReviewSerializer,
    ProductSerializer,
    SimpleUserSerializer,
)
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser, AllowAny
from api.permissions import CustomDjangoModelPermissions
from product.permissions import IsReviewAuthorOrReadOnly


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["price", "created_at"]
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]

        return [AllowAny()]

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
    permission_classes = [CustomDjangoModelPermissions]


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ProductReview.objects.none()

        return ProductReview.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_pk")
        return context

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ProductImage.objects.none()

        return ProductImage.objects.filter(product_id=self.kwargs["product_pk"])
    
    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs["product_pk"])
        serializer.save(product=product)