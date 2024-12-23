from django.urls import path

from basket.views import BasketGetAPIView

urlpatterns = [
    path("basket/", BasketGetAPIView.as_view(), name="get-basket"),
]
