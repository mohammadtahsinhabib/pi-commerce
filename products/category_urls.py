from django.urls import path
from .views import *

urlpatterns = [
    # path("categories/",ViewCategories.as_view(),name="view-category"),
    path("categories/",CategoryListCreateView.as_view(),name="view-category"),
    path("categories/<int:id>/",CategoryDetailView.as_view(),name="view-specific-category"),
]