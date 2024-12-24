from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from catalog.models import CategoryImage
from product.models import Product, Category, ProductImage, Tag, Review


class ProductDetailsAPITest(TestCase):
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

        self.product = Product.objects.create(
            category=self.category,
            price=500.67,
            count=12,
            title="Video Card",
            description="Description of the product",
            fullDescription="Full description of the product",
            freeDelivery=True,
        )

        self.image1 = ProductImage.objects.create(
            src="/media/images/image1.jpg", alt="Image 1"
        )
        self.image2 = ProductImage.objects.create(
            src="/media/images/image2.jpg", alt="Image 2"
        )
        self.product.images.add(self.image1, self.image2)

        self.tag1 = Tag.objects.create(name="Gaming")
        self.tag2 = Tag.objects.create(name="Graphics")
        self.product.tags.add(self.tag1, self.tag2)

        self.user = User.objects.create_user(username="testuser", password="password")
        self.review = Review.objects.create(
            author=self.user,
            email="no-reply@mail.ru",
            text="Great product!",
            rate=5,
        )
        self.product.reviews.add(self.review)

    def tearDown(self):
        self.category_image.src.delete(save=False)

    def test_get_product_details_success(self):
        """
        Тестирование удачного получения пользователя.
        """
        url = reverse("product-details", args=[self.product.id])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], self.product.id)
        self.assertEqual(data["category"], self.category.id)
        self.assertEqual(float(data["price"]), float(self.product.price))
        self.assertEqual(data["count"], self.product.count)
        self.assertEqual(data["title"], self.product.title)
        self.assertEqual(data["description"], self.product.description)
        self.assertEqual(data["fullDescription"], self.product.fullDescription)
        self.assertEqual(data["freeDelivery"], self.product.freeDelivery)
        self.assertEqual(len(data["images"]), 2)
        self.assertIn(self.image1.src.url, data["images"][0]["src"])
        self.assertIn(self.image2.src.url, data["images"][1]["src"])
        self.assertEqual(len(data["tags"]), 2)
        self.assertIn(self.tag1.name, data["tags"])
        self.assertIn(self.tag2.name, data["tags"])
        self.assertEqual(len(data["reviews"]), 1)
        self.assertEqual(data["reviews"][0]["author"], self.review.author.username)
        self.assertEqual(data["reviews"][0]["email"], self.review.email)
        self.assertEqual(data["reviews"][0]["text"], self.review.text)
        self.assertEqual(data["reviews"][0]["rate"], self.review.rate)

    def test_get_product_details_not_found(self):
        """
        Тестирование поведения при несуществующем id.
        """
        url = reverse("product-details", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProductReviewAPITest(TestCase):
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

        self.product = Product.objects.create(
            category=self.category,
            price=500.67,
            count=12,
            title="Video Card",
            description="Description of the product",
            fullDescription="Full description of the product",
            freeDelivery=True,
        )
        self.valid_payload = {
            "author": "Test Author",
            "email": "author@example.com",
            "text": "This is a test review.",
            "rate": 5,
        }
        self.invalid_payload = {
            "author": "",
            "email": "not-an-email",
            "text": "",
            "rate": 10,
        }

    def tearDown(self):
        self.category_image.src.delete(save=False)

    def test_create_review_valid_payload(self):
        """
        Тестирование успешного создания отзыва с валидными данными.
        """
        url = reverse("product-review", args=[self.product.id])
        response = self.client.post(url, data=self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.author, self.valid_payload["author"])
        self.assertEqual(review.email, self.valid_payload["email"])
        self.assertEqual(review.text, self.valid_payload["text"])
        self.assertEqual(review.rate, self.valid_payload["rate"])
        self.assertIn(review, self.product.reviews.all())

    def test_create_review_invalid_payload(self):
        """
        Тестирование ошибки при создании отзыва с невалидными данными.
        """
        url = reverse("product-review", args=[self.product.id])
        response = self.client.post(url, data=self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)

    def test_create_review_for_nonexistent_product(self):
        """
        Тестирование ошибки при создании отзыва для несуществующего товара.
        """
        url = reverse("product-review", args=[999])
        response = self.client.post(url, data=self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Review.objects.count(), 0)
