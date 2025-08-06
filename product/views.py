from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from product.models import Category, Product
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.


@api_view(["GET", "POST"])
def view_product(request):
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data,context ={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    product = Product.objects.select_related("category").all()

    product_data = ProductSerializer(
        product, many=True, context={"request": request}
    ).data

    return Response({"products": product_data})


@api_view(["GET", "PUT", "DELETE"])
def view_single_product(request, product_id):
    if request.method == "GET":
        product = get_object_or_404(Product, pk=product_id)
        product_data = ProductSerializer(product, context={"request": request}).data
        return Response({"product": product_data})
    elif request.method == "PUT":
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(["GET", "POST"])
def view_categories(request):

    if request.method == "POST":
        serializer = CategorySerializer(data=request.data,context = {"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    category = Category.objects.annotate(product_count = Count("products")).order_by("-id").all()
    category_data = CategorySerializer(category, many=True).data
    return Response({"categories": category_data})


@api_view()
def view_single_category(request, id):
    category = get_object_or_404(Category.objects.annotate(product_count=Count("products")), pk=id)
    category_data = CategorySerializer(category).data
    return Response({"category": category_data})
