from django.urls import path
from .views import *

urlpatterns = [
    path("", view_categories, name="view-categories"),
    path("<int:id>/", view_single_category, name="view-single-category"),
]
