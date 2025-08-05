from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # path("product/",include("product.product_urls")),
    # path("product/",include("product.category_urls")),
    # path("users/",include("users.urls")),
    path("api/", include("api.urls")),
    # path("order/",include("order.urls")),
] + debug_toolbar_urls()
