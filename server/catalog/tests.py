from django.contrib.auth.models import User
from django.db.models import Count
from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Category, CategoryImage
from catalog.serilaizers import CategorySerializer
from core.models import Tag
from product.models import Product, ProductImage, Review

from rest_framework import status
from django.urls import reverse

from product.serilaizers import ProductShortSerializers


class TestCategoriesApiView(TestCase):
    """
    Тестирование GET /api/categories/
    """

    def setUp(self):
        category_image = CategoryImage.objects.create(
            src="path/to/image.jpg", alt="Category Image"
        )
        self.category_1 = Category.objects.create(
            title="Category 1", image=category_image
        )
        self.category_2 = Category.objects.create(
            title="Category 2", image=category_image, parent=self.category_1
        )
        self.category_3 = Category.objects.create(
            title="Category 3", image=category_image, parent=self.category_1
        )
        self.client = APIClient()

    def test_get_categories(self):
        """
        Проверка на успешное получение категорий.
        """
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(
            [self.category_1, self.category_2, self.category_3], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_no_categories(self):
        """
        Проверка на получение пустого списка, при отсутствии категорий.
        """
        Category.objects.all().delete()
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class TestCatalogListAPIView(TestCase):
    """
    Тестирование GET /api/catalog/
    """
    def setUp(self):
        self.category_image = CategoryImage.objects.create(
            src="path/to/image.jpg", alt="Category Image"
        )
        self.category = Category.objects.create(
            title="Electronics", image=self.category_image
        )
        self.tag1 = Tag.objects.create(name="smartphone")
        self.tag2 = Tag.objects.create(name="laptop")

        self.image1 = ProductImage.objects.create(
            src="path/to/image1.jpg", alt="Image 1"
        )
        self.image2 = ProductImage.objects.create(
            src="path/to/image2.jpg", alt="Image 2"
        )
        self.image3 = ProductImage.objects.create(
            src="path/to/image3.jpg", alt="Image 3"
        )

        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description for product 1",
            price=100,
            count=10,
            category=self.category,
            free_delivery=True,
        )
        self.product1.images.add(self.image1, self.image2)

        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description for product 2",
            price=200,
            count=5,
            category=self.category,
            free_delivery=False,
        )
        self.product2.images.add(self.image2, self.image3)

        self.product3 = Product.objects.create(
            title="Product 3",
            description="Description for product 3",
            price=150,
            count=0,
            category=self.category,
            free_delivery=True,
        )
        self.product3.images.add(self.image1, self.image3)

        self.product1.tags.add(self.tag1)
        self.product2.tags.add(self.tag2)
        self.product3.tags.add(self.tag1, self.tag2)

    def test_get_product_list(self):
        """
        Тестирование на получение всех продуктов.
        """
        url = reverse("catalog")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)
        self.assertIn("currentPage", response.data)
        self.assertIn("lastPage", response.data)

    def test_filter_by_name(self):
        """
        Тестирование фильтра по имени.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"name": "Product 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["title"], "Product 1")

    def test_filter_by_min_price(self):
        """
        Тестирование фильтра минимальной цены.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"minPrice": 150})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

    def test_filter_by_max_price(self):
        """
        Тестирование фильтра максимальной цены.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"maxPrice": 150})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

    def test_filter_by_free_delivery(self):
        """
        Проверка фильтра бесплатной доставки.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"freeDelivery": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

    def test_filter_by_available(self):
        """
        Проверка фильтра доступных товаров.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"available": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

    def test_pagination(self):
        """
        Тестирование пагинации и лимита.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"currentPage": 1, "limit": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["currentPage"], 1)
        self.assertEqual(response.data["lastPage"], 2)

    def test_sort_by_price_dec(self):
        """
        Тестирование сортировки по цене по возрастанию.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"sort": "price", "sortType": "dec"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [item["price"] for item in response.data["items"]]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_sort_by_price_inc(self):
        """
        Тестирование сортировки по цене по убыванию.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"sort": "price", "sortType": "inc"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [item["price"] for item in response.data["items"]]
        self.assertEqual(prices, sorted(prices))

    def test_filter_by_tags(self):
        """
        Тестирование фильтрации по тегам.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"tags": ["laptop"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data["items"]:
            self.assertIn("laptop", [tag["name"] for tag in item["tags"]])

    def test_combined_filters(self):
        """
        Тестирование со всеми параметрами.
        """
        url = reverse("catalog")
        response = self.client.get(
            url,
            {
                "name": "Product 1",
                "minPrice": 100,
                "maxPrice": 200,
                "freeDelivery": True,
                "available": True,
                "sort": "price",
                "sortType": "dec",
                "tags": ["smartphone"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["title"], "Product 1")

    def test_empty_response(self):
        """
        Тестирование пустого ответа
        """
        url = reverse("catalog")
        response = self.client.get(url, {"name": "Nonexistent Product"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 0)

    def test_invalid_page(self):
        """
        Тестирование некорректного значения в параметрах пагинации.
        """
        url = reverse("catalog")
        response = self.client.get(url, {"currentPage": -1, "limit": 2})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductPopularAPIViewTest(TestCase):
    """
    Тестирование GET /api/products/popular/
    """
    def setUp(self):
        self.url = reverse("product-popular")

        self.category_image = CategoryImage.objects.create(
            src="path/to/image.jpg", alt="Category Image"
        )

        self.category = Category.objects.create(
            title="Electronics", image=self.category_image
        )

        self.tag1 = Tag.objects.create(name="smartphone")
        self.tag2 = Tag.objects.create(name="laptop")

        self.image1 = ProductImage.objects.create(
            src="path/to/image1.jpg", alt="Image 1"
        )
        self.image2 = ProductImage.objects.create(
            src="path/to/image2.jpg", alt="Image 2"
        )
        self.image3 = ProductImage.objects.create(
            src="path/to/image3.jpg", alt="Image 3"
        )

        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description for product 1",
            price=100,
            count=10,
            category=self.category,
            free_delivery=True,
        )
        self.product1.images.add(self.image1, self.image2)

        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description for product 2",
            price=200,
            count=5,
            category=self.category,
            free_delivery=False,
        )
        self.product2.images.add(self.image2, self.image3)

        self.product3 = Product.objects.create(
            title="Product 3",
            description="Description for product 3",
            price=150,
            count=0,
            category=self.category,
            free_delivery=True,
        )
        self.product3.images.add(self.image1, self.image3)

        self.product1.tags.add(self.tag1)
        self.product2.tags.add(self.tag2)
        self.product3.tags.add(self.tag1, self.tag2)

        self.user = User.objects.create_user(username="testuser", password="password")

        for i in range(5):
            Review.objects.create(
                author=self.user,
                email=f"user{i}@example.com",
                text=f"Review {i} for product 1",
                rate=4,
                date="2024-12-19T12:00:00Z",
                product=self.product1,
            )

        for i in range(3):
            Review.objects.create(
                author=self.user,
                email=f"user_review{i}@example.com",
                text="Excellent product",
                rate=5,
                date="2024-12-19T12:00:00Z",
                product=self.product2,
            )

    def test_get_popular_product(self):
        """
        Тестирование получения самого популярного товара.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        popular_product = (
            Product.objects.annotate(reviews_count=Count("reviews"))
            .order_by("-reviews_count")
            .first()
        )
        serialized_data = ProductShortSerializers(popular_product).data

        self.assertEqual(response.data, serialized_data)


class ProductLimitedAPIViewTest(TestCase):
    """
    Тестирование GET /api/products/limited/
    """
    def setUp(self):
        self.category_image = CategoryImage.objects.create(
            src="path/to/image.jpg", alt="Category Image"
        )
        self.category = Category.objects.create(
            title="Electronics", image=self.category_image
        )
        self.tag1 = Tag.objects.create(name="smartphone")
        self.tag2 = Tag.objects.create(name="laptop")

        self.image1 = ProductImage.objects.create(
            src="path/to/image1.jpg", alt="Image 1"
        )
        self.image2 = ProductImage.objects.create(
            src="path/to/image2.jpg", alt="Image 2"
        )
        self.image3 = ProductImage.objects.create(
            src="path/to/image3.jpg", alt="Image 3"
        )

        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description for product 1",
            price=100,
            count=100,
            category=self.category,
            free_delivery=True,
        )
        self.product1.images.add(self.image1, self.image2)

        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description for product 2",
            price=200,
            count=500,
            category=self.category,
            free_delivery=False,
        )
        self.product2.images.add(self.image2, self.image3)

        self.product3 = Product.objects.create(
            title="Product 3",
            description="Description for product 3",
            price=150,
            count=5,
            category=self.category,
            free_delivery=True,
        )
        self.product3.images.add(self.image1, self.image3)

        self.product1.tags.add(self.tag1)
        self.product2.tags.add(self.tag2)
        self.product3.tags.add(self.tag1, self.tag2)

        self.url = reverse("product-limited")

    def test_get_products_with_limited_stock(self):
        """
        Проверка вывода лимитированных продуктов.
        """
        response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(len(data), 1)

        product_titles = [product["title"] for product in data]
        self.assertIn("Product 3", product_titles)

    def test_get_products_no_limited_stock(self):
        """
        Проверка, что после изменения количества,
        товар не попадает в лимитированные продукты.
        """
        self.product1.count = 20
        self.product1.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        product_titles = [product["title"] for product in data]
        self.assertNotIn("Product 2", product_titles)

    def test_get_empty_list(self):
        """
        Проверка на получение пустого списка,
        при отсутствии лимитированных товаров.
        """
        Product.objects.filter(count__lt=10).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 0)
