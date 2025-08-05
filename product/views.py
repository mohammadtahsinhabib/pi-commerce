from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer,CategorySerializer
from product.models import Category, Product

# Create your views here.


@api_view()
def view_product(request):
    # Using select_related to optimize the query by fetching related category data in one go
    product = Product.objects.select_related('category').all()

    # product_data = [ProductSerializer(p).data for p in product]
    product_data = ProductSerializer(product, many=True,context = {"request":request}).data
    
    return Response({"products": product_data})


@api_view()
def view_single_product(request, id):
    product = get_object_or_404(Product,pk=id)
    product_data = ProductSerializer(product,context = {"request":request}).data
    return Response({"product": product_data})


"""
    if we don't want to use get_object_or_404, we can use try-except block
    to handle the case where the product does not exist.
    try:
        product = Product.objects.get(pk=product_id)
        product_data = {"id": product.id, "name": product.name, "price": product.price}
        return Response({"product": product_data})
    except Product.DoesNotExist:  
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
"""


@api_view()
def view_categories(request):
    category = Category.objects.all()
    category_data = CategorySerializer(category,many = True).data
    return Response({"categories": category_data})



@api_view()
def view_single_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category_data = CategorySerializer(category).data
    return Response({"category": category_data})