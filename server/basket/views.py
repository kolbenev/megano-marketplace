from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from product.models import Product
from basket.models import Basket, BasketItem
from basket.serializers import ProductInBasketSerializer


class BasketView(APIView):
    def get_basket(self, request):
        """
        Возвращает корзину текущего пользователя или создаёт новую.
        """
        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            basket, _ = Basket.objects.get_or_create(session_key=session_key)
        return basket

    def get(self, request):
        """
        Возвращает содержимое корзины.
        """
        basket = self.get_basket(request)
        basket_items = {item.product.id: item for item in basket.basket_items.all()}
        products = [item.product for item in basket.basket_items.all()]
        serializer = ProductInBasketSerializer(
            products, many=True, context={"basket_items": basket_items}
        )
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Добавляет товар в корзину.
        """
        basket = self.get_basket(request)
        product_id = request.data.get("id")
        count = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket, product=product
        )
        if not created:
            basket_item.quantity += int(count)
        else:
            basket_item.quantity = int(count)
        basket_item.save()

        return Response({"message": "Item added to basket."}, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Удаляет товар из корзины.
        """
        data = JSONParser().parse(request)
        product_id = data.get("id")
        count = data.get("count", 1)

        if not product_id:
            return Response(
                {"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        basket = self.get_basket(request)

        try:
            basket_item = BasketItem.objects.get(basket=basket, product_id=product_id)
        except BasketItem.DoesNotExist:
            return Response(
                {"error": "Item not found in basket."}, status=status.HTTP_404_NOT_FOUND
            )

        if basket_item.quantity > count:
            basket_item.quantity -= count
            basket_item.save()
            return Response(
                {"message": f"{count} item(s) removed from basket."},
                status=status.HTTP_200_OK,
            )
        else:
            basket_item.delete()
            return Response(
                {"message": "Item removed from basket."}, status=status.HTTP_200_OK
            )
