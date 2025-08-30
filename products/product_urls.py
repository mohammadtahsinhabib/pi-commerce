from django.urls import path
from .views import *

urlpatterns = [
    path("products/",view_products,name="view-product"),
    path("products/<int:id>/",view_product,name="view-specific-product"),
]