from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("api/", include("catalog.urls")),
    path("api/", include("product.urls")),
    path("api/", include("basket.urls")),
    path("api/", include("order.urls")),
    path("api/", include("tags.urls")),
    path("api/", include("userprofile.urls")),
    path("api/", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
