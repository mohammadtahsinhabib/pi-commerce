from django.urls import path
from .views import *

urlpatterns = [
    path("categories/",view_categories,name="view-category"),
    path("categories/<int:id>/",view_category,name="view-specific-category"),
]