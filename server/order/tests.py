from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import CategoryImage, Category
from order.models import Order
from product.models import ProductImage, Product


class TestOrdersApiView(APITestCase):
    def setUp(self):
        category_image_content = ContentFile(
            b"fake_image_content", "category_image.jpg"
        )
        self.category_image = CategoryImage.objects.create(
            src=category_image_content, alt="Category Image"
        )
        self.category = Category.objects.create(
            title="Electronics", image=self.category_image
        )

        product_image1_content = ContentFile(
            b"fake_image_content", "product_image1.jpg"
        )
        product_image2_content = ContentFile(
            b"fake_image_content", "product_image2.jpg"
        )
        self.image1 = ProductImage.objects.create(
            src=product_image1_content, alt="Image 1"
        )
        self.image2 = ProductImage.objects.create(
            src=product_image2_content, alt="Image 2"
        )

        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description for product 1",
            price=100,
            count=100,
            category=self.category,
            freeDelivery=True,
        )
        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description for product 2",
            price=100,
            count=100,
            category=self.category,
            freeDelivery=True,
        )

        self.order1 = Order.objects.create(
            fullName="John Doe",
            email="john@example.com",
            phone="123456789",
            deliveryType="courier",
            paymentType="cash",
            totalCost=500.00,
            status="accepted",
            city="Moscow",
            address="Red Square 1",
        )
        self.order2 = Order.objects.create(
            fullName="Jane Smith",
            email="jane@example.com",
            phone="987654321",
            deliveryType="pickup",
            paymentType="online",
            totalCost=300.00,
            status="processing",
            city="Saint Petersburg",
            address="Nevsky Prospect 25",
        )
        self.order1.products.add(self.product1)
        self.order2.products.add(self.product2)

    def tearDown(self):
        self.image1.src.delete(save=False)
        self.image2.src.delete(save=False)
        self.category_image.src.delete(save=False)

    def test_get_orders(self):
        """
        GET /orders Тестируем получение списка заказов.
        """
        list_url = reverse("orders")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        first_order = response.data[0]
        expected_keys = {
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        }
        self.assertTrue(expected_keys.issubset(first_order.keys()))

    def test_create_order(self):
        """
        POST /orders/ Тестирование создания нового заказа.
        """
        list_url = reverse("orders")
        data = {
            "fullName": "Alice Cooper",
            "email": "alice@example.com",
            "phone": "111222333",
            "deliveryType": "courier",
            "paymentType": "online",
            "totalCost": 250.00,
            "status": "processing",
            "city": "Moscow",
            "address": "Tverskaya 1",
            "products": [self.product1.id],
        }
        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["fullName"], "Alice Cooper")
        self.assertEqual(response.data["email"], "alice@example.com")
        self.assertEqual(response.data["status"], "processing")

    def test_get_order(self):
        """
        GET /orders/{id} Тестирование получение одного заказа по ID.
        """
        order_url = reverse("order-details", args=[self.order1.id])
        response = self.client.get(order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order1.id)
        self.assertEqual(response.data["status"], "accepted")
        self.assertEqual(len(response.data["products"]), 1)

    def test_confirm_order(self):
        """
        POST /orders/{id} Тестирование потдверждения заказа.
        """
        order_url = reverse("order-details", args=[self.order2.id])
        response = self.client.post(order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "accepted")
