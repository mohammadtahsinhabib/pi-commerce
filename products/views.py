from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

@api_view()
def view_products(request):
    product = Product.objects.all()
    serialize = ProductSerializer(product,many = True)
    return Response(serialize.data)

@api_view()
def view_product(request,id):
    product = get_object_or_404(Product,id=id)
    serialize = ProductSerializer(product)
    return Response(serialize.data)

@api_view()
def view_category(request):
    return Response("category")