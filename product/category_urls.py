from django.urls import path
from .views import *

urlpatterns = [
    path("", view_categories, name="view-categories"),
]
