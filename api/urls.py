from django.urls import include, path
from rest_framework_nested import routers

from order.views import CartViewSet, CartItemViewSet
from product.views import CategoriesViewSet, ProductReviewViewSet, ProductsViewSet

router = routers.DefaultRouter()
router.register("products", ProductsViewSet, basename="product")
router.register("categories", CategoriesViewSet, basename="category")
router.register("cart", CartViewSet, basename="cart")


product_routers = routers.NestedDefaultRouter(router, "products", lookup="product")
product_routers.register("reviews", ProductReviewViewSet, basename="product-reviews")


cart_routers = routers.NestedDefaultRouter(router, "cart", lookup="cart")
cart_routers.register("items", CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_routers.urls)),
    path("", include(cart_routers.urls)),
]
