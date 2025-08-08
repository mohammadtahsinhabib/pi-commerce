from django.urls import path

from .views import *

urlpatterns = [
    path("", ViewProducts.as_view(), name="view-products"),
    path("<int:product_id>/", ViewSingleProduct.as_view(), name="view-single-product"),
]
