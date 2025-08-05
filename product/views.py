from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from product.models import Category, Product
# Create your views here.

@api_view()
def view_product(request):
    product = Product.objects.all()
    product_data = [{"id": p.id, "name": p.name, "price": p.price} for p in product]
    return Response({"products": product_data})

@api_view()
def view_single_product(request, product_id):
    product = Product.objects.get_or_404(pk=product_id)
    product_data = {"id": product.id, "name": product.name, "price": product.price}
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

    return Response({"message":2})