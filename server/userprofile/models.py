from django.contrib.auth.models import AbstractUser, User
from django.db import models


class ProfileAvatar(models.Model):
    src = models.ImageField(upload_to="media/images/profile/", null=True, blank=True)
    alt = models.CharField(max_length=50, blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    avatar = models.OneToOneField(
        ProfileAvatar, on_delete=models.CASCADE, null=True, blank=True
    )
