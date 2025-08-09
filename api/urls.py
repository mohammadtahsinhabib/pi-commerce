from rest_framework_nested import routers
from product.views import ProductsViewSet, CategoriesViewSet , ProductReviewViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register("products", ProductsViewSet, basename="product")
router.register("categories", CategoriesViewSet, basename="category")

product_routers = routers.NestedDefaultRouter(router, "products", lookup="product")

product_routers.register("reviews", ProductReviewViewSet, basename="product-reviews")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_routers.urls)),
]
