from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


class ViewProducts(APIView):
    """
        GET: List all products
        POST: Create a new product
    """

    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ViewProduct(APIView):
    """
    GET: Retrieve a product
    PUT: Update a product
    DELETE: Delete a product
    """

    def get_object(self, id):
        return get_object_or_404(Product, id=id)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer

class ViewCategories(APIView):
    """
    GET: List all categories with product counts
    POST: Create a new category
    """

    def get(self, request):
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewCategory(APIView):
    """
    GET: Retrieve a single category with product count
    """

    def get(self, request, id):
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count("products")), id=id
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data)