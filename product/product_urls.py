from django.urls import path
from .views import *

urlpatterns = [
    path('', view_product, name='view-product'),
]