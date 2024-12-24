from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User

from basket.models import Basket, BasketItem
from catalog.models import Category
from product.models import Product


class BasketViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='category')
        self.username = "testuser"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.product1 = Product.objects.create(
            id=1, title="Product 1", price=100.0, category=self.category, description="Test product 1"
        )
        self.product2 = Product.objects.create(
            id=2, title="Product 2", price=200.0, category=self.category, description="Test product 2"
        )
        self.basket = Basket.objects.create(user=self.user)
        self.client.login(username=self.username, password=self.password)
        self.basket_url = reverse("basket")

    def test_get_basket(self):
        """
        Тест получения содержимого корзины.
        """
        BasketItem.objects.create(basket=self.basket, product=self.product1, quantity=2)
        BasketItem.objects.create(basket=self.basket, product=self.product2, quantity=1)
        response = self.client.get(self.basket_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.product1.id)
        self.assertEqual(response.data[0]["count"], 2)
        self.assertEqual(response.data[1]["id"], self.product2.id)
        self.assertEqual(response.data[1]["count"], 1)

    def test_post_add_item_to_basket(self):
        """
        Тест добавления товара в корзину.
        """
        data = {"id": self.product1.id, "count": 3}
        response = self.client.post(self.basket_url, data)
        basket_item = BasketItem.objects.get(basket=self.basket, product=self.product1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(basket_item.quantity, 3)

    def test_post_update_existing_item_in_basket(self):
        """
        Тест обновления количества товара в корзине.
        """
        BasketItem.objects.create(basket=self.basket, product=self.product1, quantity=2)
        data = {"id": self.product1.id, "count": 3}
        response = self.client.post(self.basket_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        basket_item = BasketItem.objects.get(basket=self.basket, product=self.product1)
        self.assertEqual(basket_item.quantity, 5)

    def test_delete_item_from_basket(self):
        """
        Тест удаления товара из корзины.
        """
        BasketItem.objects.create(basket=self.basket, product=self.product1, quantity=5)

        data = {"id": self.product1.id, "count": 3}
        response = self.client.delete(self.basket_url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        basket_item = BasketItem.objects.get(basket=self.basket, product=self.product1)
        self.assertEqual(basket_item.quantity, 2)

        data = {"id": self.product1.id, "count": 2}
        response = self.client.delete(self.basket_url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(BasketItem.DoesNotExist):
            BasketItem.objects.get(basket=self.basket, product=self.product1)

    def test_delete_item_not_in_basket(self):
        """
        Тест удаления несуществующего товара из корзины.
        """
        data = {"id": 999, "count": 1}
        response = self.client.delete(self.basket_url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Item not found in basket.")
