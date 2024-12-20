from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from order.serilaizers import OrderSerializer


class OrderApiView(APIView):
    def get(self, request: Request) -> Response:
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsApiView(APIView):
    def get(self, request: Request, id: int) -> Response:
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request, id: int) -> Response:
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(order)
        order.status = "accepted"
        order.save()
        return Response(serializer.data, status.HTTP_200_OK)
