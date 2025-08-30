from django.urls import path
from .views import *

urlpatterns = [
    path("products/",ProductListCreateView.as_view(),name="view-product"),
    path("products/<int:id>/",ProductDetailView.as_view(),name="view-specific-product"),
]