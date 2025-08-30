from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/",include("products.product_urls")),
    path("api/v1/",include("products.category_urls")),
    
]+ debug_toolbar_urls()
