from django.urls import path

from product.views import ProductDetailsAPIView, ProductReviewAPIVIew


urlpatterns = [
    path("product/<int:id>/", ProductDetailsAPIView.as_view(), name="product-details"),
    path(
        "product/<int:id>/reviews/",
        ProductReviewAPIVIew.as_view(),
        name="product-review",
    ),
]
