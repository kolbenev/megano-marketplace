from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import Basket
from product.models import Product
from product.serializers import ProductShortSerializers


class BasketGetAPIView(APIView):
    def get(self, request: Request) -> Response:
        basket = Basket.objects.filter(user=self.request.user)
        products = basket.products
        data = ProductShortSerializers(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)
