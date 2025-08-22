
from django.urls import include, path
from rest_framework_nested import routers
from order.views import CartViewSet, CartItemViewSet, OrderViewSet
from product.views import CategoriesViewSet, ProductReviewViewSet, ProductsViewSet, ProductImageViewSet 

router = routers.DefaultRouter()
router.register("products", ProductsViewSet, basename="product")
router.register("categories", CategoriesViewSet, basename="category")
router.register("cart", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename="orders")


product_routers = routers.NestedDefaultRouter(router, "products", lookup="product")
product_routers.register("reviews", ProductReviewViewSet, basename="product-reviews")
product_routers.register("images", ProductImageViewSet, basename="product-images")


cart_routers = routers.NestedDefaultRouter(router, "cart", lookup="cart")
cart_routers.register("items", CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_routers.urls)),
    path("", include(cart_routers.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
