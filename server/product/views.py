from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Review
from product.serializers import ProductFullSerializers, ReviewSerializer


class ProductDetailsAPIView(APIView):
    """
    Получение полной информации о продукте.
    """

    def get(self, request: Request, id: int) -> Response:
        product = get_object_or_404(
            Product.objects.annotate(rating=Avg("reviews__rate")), id=id
        )
        serializer = ProductFullSerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewAPIVIew(APIView):
    """
    Сделать отзыв на товар.
    """

    def post(self, request: Request, id: int) -> Response:
        permission_classes = [IsAuthenticated]
        product = get_object_or_404(Product, id=id)
        request_serializer = ReviewSerializer(data=request.data)
        if request_serializer.is_valid():
            review = request_serializer.save()
            product.reviews.add(review)
            return Response(request_serializer.data, status=status.HTTP_200_OK)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
