from django.urls import path
from .views import (
    CategoriesApiView,
    CatalogListAPIView,
    ProductPopularAPIView,
    ProductLimitedAPIView,
    SalesListAPIView,
    BannersListAPIView,
)

urlpatterns = [
    path("categories/", CategoriesApiView.as_view(), name="categories"),
    path("catalog/", CatalogListAPIView.as_view(), name="catalog"),
    path("products/popular/", ProductPopularAPIView.as_view(), name="product-popular"),
    path("products/limited/", ProductLimitedAPIView.as_view(), name="product-limited"),
    path("sales/", SalesListAPIView.as_view(), name="sales"),
    path("banners/", BannersListAPIView.as_view(), name="banners"),
]
