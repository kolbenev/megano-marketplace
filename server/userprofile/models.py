from django.contrib.auth.models import AbstractUser, User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    avatar_src = models.ImageField(
        upload_to="media/images/profile/", null=True, verbose_name="Avatar Image"
    )
    avatar_alt = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Avatar Alt Text"
    )

