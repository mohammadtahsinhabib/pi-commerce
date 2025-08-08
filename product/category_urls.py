from django.urls import path

from .views import *

urlpatterns = [
    path("", ViewCategories.as_view(), name="view-categories"),
    path("<int:id>/", ViewSingleCategory.as_view(), name="view-single-category"),
]
