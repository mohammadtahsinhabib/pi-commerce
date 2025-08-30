from django.urls import path
from .views import *

urlpatterns = [
    path("products/",ViewProducts.as_view(),name="view-product"),
    path("products/<int:id>/",ViewProduct.as_view(),name="view-specific-product"),
]