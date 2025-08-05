from django.urls import path
from .views import *

urlpatterns = [
    path("", view_product, name="view-product"),
    path("<int:pk>/", view_single_product, name="view-single-product"),
]
