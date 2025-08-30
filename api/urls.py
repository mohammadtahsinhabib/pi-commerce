from django.urls import path, include
from products.views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet,basename="categories")

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]