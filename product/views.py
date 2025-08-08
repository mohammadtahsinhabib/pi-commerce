from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from django.db.models import Count
from product.models import Category, Product
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView

# Create your views here.

class ViewProducts(APIView):

    def get(self, request):
        product = Product.objects.select_related("category").all()
        product_data = ProductSerializer(
            product, many=True, context={"request": request}
        ).data
        return Response({"products": product_data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewSingleProduct(APIView):

    def get(self, request, product_id):
        product = get_object_or_404(Product.objects.select_related("category"), pk=product_id)
        product_data = ProductSerializer(product, context={"request": request}).data
        return Response({"product": product_data})

    def put(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ViewCategories(APIView):

    def get(self, request):
        category = Category.objects.annotate(product_count=Count("products")).order_by("-id").all()
        category_data = CategorySerializer(category, many=True, context={"request": request}).data
        return Response({"categories": category_data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ViewSingleCategory(APIView):

    def get(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count=Count("products")), pk=id)
        category_data = CategorySerializer(category, context={"request": request}).data
        return Response({"category": category_data})
    
    def put(self, request, id):
        category = get_object_or_404(Category, pk=id)
        serializer = CategorySerializer(category, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        category = get_object_or_404(Category, pk=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    