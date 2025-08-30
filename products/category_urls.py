from django.urls import path
from .views import *

urlpatterns = [
    path("categories/",view_category,name="view-category")
]