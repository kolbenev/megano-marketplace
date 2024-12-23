from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from userprofile.models import UserProfile, ProfileAvatar


class TestProfileGetAPI(TestCase):
    def setUp(self):
        avatar_file = ContentFile(b"fake_image_content", "category_image.jpg")
        self.avatar = ProfileAvatar.objects.create(
            src=avatar_file, alt="Image alt string"
        )
        self.url = reverse("profile")
        self.username = "testuser"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fullName="Annoying Orange",
            email="no-reply@mail.ru",
            phone="88002000600",
            avatar=self.avatar,
        )

    def tearDown(self):
        self.avatar.src.delete(save=False)

    def test_get_profile_authenticated(self):
        """
        Тестирование верного получения данных.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "fullName": self.profile.fullName,
            "email": self.profile.email,
            "phone": self.profile.phone,
            "avatar": {"src": self.avatar.src.url, "alt": self.avatar.alt},
        }
        self.assertEqual(response.json(), expected_data)


class TestProfilePostAPI(TestCase):
    def setUp(self):
        avatar_file = ContentFile(b"fake_image_content", "category_image.jpg")
        self.avatar = ProfileAvatar.objects.create(
            src=avatar_file, alt="Image alt string"
        )
        self.url = reverse("profile")
        self.username = "testuser"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fullName="Annoying Orange",
            email="no-reply@mail.ru",
            phone="88002000600",
            avatar=self.avatar,
        )

    def tearDown(self):
        self.avatar.src.delete(save=False)

    def test_update_profile_success(self):
        """
        Тестирование обновления информации о профиле пользователя.
        """
        self.client.login(username=self.username, password=self.password)
        updated_data = {
            "fullName": "Updated Orange",
            "email": "updated@mail.ru",
            "phone": "88002222333",
        }
        response = self.client.post(self.url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.fullName, updated_data["fullName"])
        self.assertEqual(self.profile.email, updated_data["email"])
        self.assertEqual(self.profile.phone, updated_data["phone"])

    def test_update_profile_invalid_data(self):
        """
        Проверка обработки неверных данных при обновлении профиля.
        """
        self.client.login(username=self.username, password=self.password)

        invalid_data = {
            "fullName": "",
            "email": "updated@mail.ru",
            "phone": "88002222333",
        }
        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fullName", response.json())


class TestUpdateAvatarView(TestCase):
    def setUp(self):
        avatar_file = ContentFile(b"fake_image_content", "image.jpg")
        self.new_avatar_file = ContentFile(b"new_image_content", "new_image.jpg")

        self.avatar = ProfileAvatar.objects.create(
            src=avatar_file, alt="Image alt string"
        )
        self.url = reverse("profile")
        self.username = "testuser"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fullName="Annoying Orange",
            email="no-reply@mail.ru",
            phone="88002000600",
            avatar=self.avatar,
        )

    def tearDown(self):
        self.avatar.src.delete(save=False)

    def test_update_avatar_success(self):
        """
        Проверка успешного обновления аватара пользователя.
        """
        self.client.login(username=self.username, password=self.password)
        update_data = {
            "avatar": self.new_avatar_file,
        }
        response = self.client.post(self.url, data=update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.avatar.src, "media/images/profile/image.jpg")

    def test_update_avatar_without_file(self):
        """
        Проверка, что если аватар не был предоставлен, возвращается ошибка 404.
        """
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_avatar_unauthenticated(self):
        """
        Тестирование обновление аватарки. неаутентифицированный пользовательем.
        """
        update_data = {
            "avatar": self.new_avatar_file,
        }
        response = self.client.post(self.url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
