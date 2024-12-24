from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from tags.models import Tag


class TestTagsDetails(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Gaming")
        self.tag2 = Tag.objects.create(name="Work")
        self.tag3 = Tag.objects.create(name="Leisure")

        self.url = reverse("tags")
        self.client = APIClient()

    def test_tag_correct(self):
        """
        Тест успешного запроса.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["name"], "Gaming")
        self.assertEqual(response.data[1]["name"], "Work")
        self.assertEqual(response.data[2]["name"], "Leisure")

    def test_empty_tags(self):
        """
        Тестирование пустого запроса.
        """
        Tag.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
