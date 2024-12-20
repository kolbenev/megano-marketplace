from django.urls import path
from order.views import OrderApiView, OrderDetailsApiView


urlpatterns = [
    path("orders", OrderApiView.as_view(), name="orders"),
    path("order/<int:id>", OrderDetailsApiView.as_view(), name="order-details"),
]
